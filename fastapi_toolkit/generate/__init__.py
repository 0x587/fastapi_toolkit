import datetime
import os
import hashlib
from collections import defaultdict

import typer
from typing import Callable, Any, Sequence, Dict, List, Optional, Tuple, Literal, Type
from jinja2 import Environment, PackageLoader
import networkx as nx

from pydantic import BaseModel, Field as PField
from fastapi_toolkit.define import Schema
from .field_helper import FieldHelper, FieldType, LinkType

from .sql_mapping import mapping
from .utils import to_snake, plural

GENERATE_FUNC = Callable[[], str]


class NameInfo(BaseModel):
    origin: str
    snake: str
    snake_plural: str
    camel: str
    camel_plural: str
    table: str
    db: str
    schema: str
    base_schema: str
    fk: str


class FK(BaseModel):
    name: str
    key_type: str = "int"
    column: str


class AssociationTable(BaseModel):
    name: str
    left: 'ModelRenderData'
    right: 'ModelRenderData'


class LinkRenderData(BaseModel):
    link_name: str
    target_type: str
    back_populates: str

    schema_link_name: str
    schema_target_type: str


class Link(BaseModel):
    link_name: str
    origin: "ModelRenderData"
    target: "ModelRenderData"
    fk: Optional[FK] = None
    table: Optional[AssociationTable] = None
    type: LinkType

    render_data: Optional[LinkRenderData] = None

    def make_render(self, pair_link: "Link"):
        self.render_data = LinkRenderData(link_name=self.link_name, target_type=self.target.name.db,
                                          back_populates=pair_link.link_name,
                                          schema_link_name=self.link_name,schema_target_type=self.target.name.base_schema)
        if self.type == LinkType.many:
            self.render_data.target_type = f'List[{self.render_data.target_type}]'

    # t1: Literal["one", "many"]
    # t2: Optional[Literal["one", "many"]]
    # m1: 'ModelRenderData'
    # m2: 'ModelRenderData'
    # nullable: bool

    def link_prefix(self):
        if self.type == "one":
            target_name = self.target.name.snake
        else:
            target_name = self.target.name.snake_plural
        if self.link_name[-len(target_name):] != target_name:
            raise ValueError(f"link name {self.link_name} not match target {self.target.name.origin}")
        return self.link_name[:-len(target_name)]


class Field(BaseModel):
    name: NameInfo
    type: FieldType


class ModelRenderData(BaseModel):
    name: NameInfo
    model: Type[Schema] = None
    fields: List[Field] = []
    links: List[Link] = []


class CodeGenerator:
    def __init__(self, root_path='inner_code'):
        self.root_path = root_path
        self.models_path = os.path.join(root_path, 'models.py')
        self.schemas_path = os.path.join(root_path, 'schemas.py')
        self.dev_path = os.path.join(root_path, 'dev')
        self.crud_path = os.path.join(root_path, 'crud')
        self.routers_path = os.path.join(root_path, 'routers')
        self.auth_path = os.path.join(root_path, 'auth')

        self.force_rewrite = False

        if not os.path.exists(self.root_path):
            os.mkdir(self.root_path)
        if not os.path.exists(self.dev_path):
            os.mkdir(self.dev_path)
        if not os.path.exists(self.crud_path):
            os.mkdir(self.crud_path)
        if not os.path.exists(self.routers_path):
            os.mkdir(self.routers_path)
        if not os.path.exists(self.auth_path):
            os.mkdir(self.auth_path)
        self.env = Environment(
            loader=PackageLoader('fastapi_toolkit', 'templates'),
            trim_blocks=True, lstrip_blocks=True)

        self.define_schemas: Dict[str, Type[Schema]] = {}
        self.pydantic_schemas: Dict[str, Type[Schema]] = {}
        self.links: List[Tuple[Literal["one"] | Literal["many"], Type[Schema], Type[Schema]]] = []
        self.custom_types: List[Dict[str, Any]] = []
        self.model_network = nx.Graph()
        self.association_tables: List[AssociationTable] = []

    @staticmethod
    def _check_file_valid(path):
        with open(path, 'r') as f:
            line = f.readline()
            if not line.startswith('# generate_hash:'):
                return False
            content_hash = line.split(':')[1].strip()
            f.readline()
            f.readline()
            f.readline()
            content = f.read()
            return hashlib.md5(content.encode('utf8')).hexdigest() == content_hash

    def _generate_file(self, path, func: GENERATE_FUNC):
        content = func()
        generate_hash = hashlib.md5(content.encode('utf8')).hexdigest()
        if os.path.exists(path):
            with open(path, 'r') as f:
                line = f.readline()
                if line.startswith('# generate_hash:'):
                    head_hash = line.split(':')[1].strip()
                else:
                    head_hash = None
                if head_hash == generate_hash and CodeGenerator._check_file_valid(path):
                    print(f'file {path} is up to date, skip generate')
                    return
                elif not self.force_rewrite:
                    overwrite = typer.confirm(
                        f'file {path} has been changed or is out of date, do you want to overwrite it?')
                    if not overwrite:
                        return
        with open(path, 'w') as f:
            f.write(f'# generate_hash: {generate_hash}\n')
            f.write(f'"""\n'
                    f'This file was automatically generated in {datetime.datetime.now()}\n'
                    f'"""\n')
            f.write(content)

    def parse(self):
        self._parse_models()
        self._parse_mock()

    def _get_schemas(self, root=Schema):
        for model_ in root.__subclasses__():
            yield model_
            yield from self._get_schemas(model_)

    def _parse_models(self):
        self.define_schemas = {schema.__name__: schema for schema in self._get_schemas()}
        self.model_render_data = {
            schema_name: self._make_render_data_field(schema)
            for schema_name, schema in self.define_schemas.items()
        }
        # TODO: build link
        self.build_links()
        # for render_data in self.model_render_data.values():
        #     for l1 in render_data.links:
        #         for l2 in self.model_render_data[l1.m2.name.camel].links:
        #             if l2.m2.name.camel != render_data.name.camel:
        #                 continue
        #             l1.t2 = l2.t1
        #             l2.t2 = l1.t1
        #             break

    def build_links(self):
        links: Dict[str, List[Link]] = defaultdict(list)
        for model in self.model_render_data.values():
            for field in filter(lambda x: x.type.link is not None, model.fields):
                link = Link(link_name=field.name.origin, origin=model,
                            target=self.model_render_data[field.type.link.model], type=field.type.link.type)
                links[model.name.origin].append(link)
            model.fields = list(filter(lambda x: x.type.link is None, model.fields))

        link_groups: List[Tuple[Link, Link]] = []
        visited_link = set()
        for ls in links.values():
            for link in ls:
                if id(link) in visited_link:
                    continue
                target_links = links[link.target.name.origin]
                for target_link in target_links:
                    if id(target_link) in visited_link:
                        continue
                    if (link.link_prefix() == target_link.link_prefix()
                            and link.target.name.origin == target_link.origin.name.origin
                            and target_link.target.name.origin == link.origin.name.origin):
                        visited_link.add(id(link))
                        visited_link.add(id(target_link))
                        link_groups.append((link, target_link))
                        break
                else:
                    raise ValueError(f"unable to pair link {link.link_name} to target {link.target.name.origin}")

        def make_one_many_link(l_one: Link, l_many: Link):
            l_one.fk = FK(name=f'_fk_{l_one.link_name}_{l_one.target.name.table}_id',
                          column=f"{l_one.target.name.table}.id")
            l_one.origin.links.append(l_one)
            l_many.origin.links.append(l_many)
            l_one.make_render(l_many)
            l_many.make_render(l_one)

        for l1, l2 in link_groups:
            t1, t2 = l1.type, l2.type
            match (t1, t2):
                case (LinkType.one, LinkType.one):
                    l1.origin.links.append(l1)
                    l2.origin.links.append(l2)
                    l1.fk = FK(name=f'_fk_{l1.link_name}_{l1.target.name.table}_id',
                               column=f'{l1.target.name.table}.id')
                    l1.make_render(l2)
                    l2.make_render(l1)
                case (LinkType.one, LinkType.many):
                    make_one_many_link(l1, l2)
                case (LinkType.many, LinkType.one):
                    make_one_many_link(l2, l1)
                case (LinkType.many, LinkType.many):
                    at_name = ['association_table']
                    if l1.link_prefix() != "":
                        at_name.append(l1.link_prefix().replace('_', ''))
                    at_name += [l1.origin.name.table, l2.origin.name.table]
                    association_table = AssociationTable(
                        name='_'.join(at_name),
                        left=l1.origin, right=l2.origin
                    )
                    l1.table = association_table
                    l2.table = association_table
                    self.association_tables.append(association_table)
                    l1.origin.links.append(l1)
                    l2.origin.links.append(l2)
                    l1.make_render(l2)
                    l2.make_render(l1)

    def _make_render_data_field(self, schema: Type[Schema]):
        fh = FieldHelper()

        return ModelRenderData(
            name=self._name_info(schema.__name__),
            fields=[Field(name=self._name_info(name), type=fh.parse(field.annotation)) for name, field in
                    schema.model_fields.items()]
        )

    def _parse_mock(self, export=False):
        self.model_network.add_nodes_from(self.model_render_data.keys())
        self.mock_dependency = {}
        self.mock_root = []
        for component_nodes in nx.connected_components(self.model_network):
            subgraph = self.model_network.subgraph(component_nodes)
            mst = nx.minimum_spanning_tree(subgraph)
            max_degree_node = max(subgraph.degree, key=lambda x: x[1])[0]
            rooted_tree = nx.dfs_tree(mst, source=max_degree_node)
            if export:
                import matplotlib.pyplot as plt
                pos = nx.planar_layout(self.model_network)
                nx.draw(rooted_tree.to_directed(), pos, with_labels=True)
                plt.show()
            self.mock_root.append(max_degree_node)
            for node in rooted_tree.nodes():
                self.mock_dependency[node] = list(rooted_tree.successors(node))

    @staticmethod
    def _name_info(name) -> NameInfo:
        return NameInfo(
            origin=name,
            snake=to_snake(name),
            snake_plural=plural(to_snake(name)),
            camel=name,
            camel_plural=plural(name),
            table=to_snake(name),
            db=f'DB{name}',
            schema=f'Schema{name}',
            base_schema=f'SchemaBase{name}',
            fk=f'fk_{to_snake(name)}_id',
        )

    # def _make_field(self, name, field_info):
    #     type_ = field_info.annotation
    #     is_custom, sql_type_ = mapping(type_)
    #     if type_.__module__ != 'builtins':
    #         type_str = f'{type_.__module__}.{type_.__name__}'
    #     else:
    #         type_str = type_.__name__
    #     res = {
    #         'name': self._name_info(name),
    #         'type': type_str,
    #         'sql_type': sql_type_,
    #         'default': field_info.default,
    #         'default_factory': field_info.default_factory,
    #         'nullable': not field_info.is_required(),
    #         'alias': field_info.alias,
    #     }
    #
    #     # custom type
    #     if is_custom:
    #         import importlib.util
    #         import sys
    #         spec = importlib.util.spec_from_file_location("metadata.models", os.getcwd() + '/metadata/models.py')
    #         models = importlib.util.module_from_spec(spec)
    #         sys.modules["metadata.models"] = models
    #         spec.loader.exec_module(models)
    #         cls = getattr(models, type_.__name__)
    #         module_path = os.path.abspath(inspect.getfile(cls))
    #         current_directory = os.getcwd()
    #         import_path, _ = os.path.splitext(os.path.relpath(module_path, current_directory))
    #         self.custom_types.append({
    #             'name': type_.__name__,
    #             'source': inspect.getsource(cls),
    #             'import_path': import_path.replace(os.path.sep, '.')
    #         })
    #
    #     return res

    # def _make_render_data(self, model_name: str, model_: Type[Schema],
    #                       d: Dict[str, ModelRenderData]) -> ModelRenderData:
    #     def is_model(t: Type) -> bool:
    #         return isinstance(t, type) and Schema.__subclasscheck__(t)
    #
    #     def is_batch_model(t: Type) -> bool:
    #         if hasattr(t, '__origin__') and Sequence.__subclasscheck__(
    #                 getattr(t, '__origin__')):
    #             seq_member: Type[Schema] = getattr(t, '__args__')[0]
    #             return is_model(seq_member)
    #         return False
    #
    #     model = d[model_name]
    #     for name, field in model_.model_fields.items():
    #         if name in ['id']:
    #             raise ValueError(f'{model_name}.{name} is reserved')
    #
    #         field_type: Type[Schema] | None = field.annotation
    #         if field_type is None:
    #             raise ValueError(f'{model_name}.{name} missing type hint')
    #
    #         if is_model(field_type):
    #             model.links.append(Link(
    #                 link_name=name,
    #                 t1='one', t2=None, m1=model, m2=d[field_type.__name__],
    #                 nullable=not field.is_required()))
    #             self.model_network.add_edge(model.name.camel, d[field_type.__name__].name.camel)
    #             continue
    #
    #         if is_batch_model(field_type):
    #             model.links.append(Link(
    #                 link_name=name,
    #                 t1="many", t2=None, m1=model, m2=d[getattr(field_type, '__args__')[0].__name__],
    #                 nullable=not field.is_required()))
    #             continue
    #
    #         model.fields.append(self._make_field(name, field))
    #     return model

    def _define2table(self) -> str:
        template = self.env.get_template('models/main.py.jinja2')
        return template.render(
            deps=self.custom_types,
            models=self.model_render_data.values(),
            association_tables=self.association_tables,
        )

    def _define2schema(self) -> str:
        template = self.env.get_template('schemas/main.py.jinja2')
        return template.render(
            deps=self.custom_types,
            models=self.model_render_data.values(),
        )

    def _from_template(self, template_name: str, **kwargs):
        def func():
            return self.env.get_template(template_name).render(**kwargs)

        return func

    def _generate_tables(self, auth_type):
        self._generate_file(os.path.join(self.root_path, 'db.py'), self._from_template('db.py.jinja2'))
        self._generate_file(os.path.join(self.root_path, 'setting.py'),
                            self._from_template('setting.py.jinja2', auth_type=auth_type))
        self._generate_file(self.models_path, self._define2table)
        self._generate_file(self.schemas_path, self._define2schema)
        self._generate_file(
            os.path.join(self.dev_path, 'db.py'),
            self._from_template(
                'dev.db.py.jinja2',
                root_path=str(self.root_path).replace('/', '.').replace('\\', '.')))
        self._generate_file(os.path.join(self.dev_path, '__init__.py'), lambda: '')

    def _generate_routers(self):
        for model in self.model_render_data.values():
            if model.name.camel == 'User':
                continue
            self._generate_file(os.path.join(self.crud_path, f'{model.name.snake}_crud.py'),
                                self._from_template('crud/main.py.jinja2', model=model))
            self._generate_file(os.path.join(self.routers_path, f'{model.name.snake}_router.py'),
                                self._from_template('routers/main.py.j2', model=model))
        self._generate_file(os.path.join(self.routers_path, '__init__.py'), self._from_template(
            'routers/init.py.j2',
            models=list(filter(lambda x: x.name.camel != 'User', self.model_render_data.values()))
        ))
        self._generate_file(os.path.join(self.crud_path, '__init__.py'), lambda: '')

    def _generate_mock(self):
        self._generate_file(
            os.path.join(self.root_path, 'mock.py'), self._from_template(
                'mock.py.j2',
                deps=self.mock_dependency,
                mock_root=self.mock_root,
                models=self.model_render_data.values()))

    def _generate_auth(self, mode: str):
        user_model = self.model_render_data['User']
        self._generate_file(os.path.join(self.auth_path, '__init__.py'),
                            self._from_template(f'auth/{mode}/__init__.py.j2'))
        self._generate_file(os.path.join(self.auth_path, 'models.py'),
                            self._from_template(f'auth/{mode}/models.py.j2', model=user_model))
        self._generate_file(os.path.join(self.auth_path, 'routes.py'), self._from_template(f'auth/{mode}/routes.py.j2'))

    def _generate_config(self):
        self._generate_file(os.path.join(self.root_path, 'config.py'), self._from_template(
            'config.py.j2', models=self.model_render_data.values()))

    def _generate_custom_types(self):
        self._generate_file(os.path.join(self.root_path, 'custom_types.py'), self._from_template(
            'custom_types.py.j2', custom_types=self.custom_types))

    def generate(self, table: bool = True, router: bool = True, mock: bool = True, auth: str = ""):
        self.parse()
        self._generate_custom_types()
        if table:
            self._generate_tables(auth_type=auth)
        # if router:
        #     self._generate_routers()
        # if mock:
        #     self._generate_mock()
        # if auth != "":
        #     self._generate_auth(mode=auth)
        # self._generate_config()
