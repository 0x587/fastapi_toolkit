import datetime
import os
import hashlib
import typer
from typing import Callable, Any, Sequence, Dict, List, Optional, Tuple, Literal, Type
from jinja2 import Environment, PackageLoader
import networkx as nx

from pydantic import BaseModel
from fastapi_toolkit.define import Schema

from .sql_mapping import mapping
from .utils import to_snake, plural

GENERATE_FUNC = Callable[[Any, ...], str]


class NameInfo(BaseModel):
    snake: str
    snake_plural: str
    camel: str
    camel_plural: str
    table: str
    db: str
    schema: str
    base_schema: str
    fk: str


class Link(BaseModel):
    t1: Literal["one", "many"]
    t2: Optional[Literal["one", "many"]]
    m1: 'ModelRenderData'
    m2: 'ModelRenderData'
    nullable: bool


class ModelRenderData(BaseModel):
    name: NameInfo
    model: Type[Schema] = None
    fields: List[Dict[str, Any]] = []
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
        self.links: List[Tuple[Literal["one"] | Literal["many"], Type[Schema], Type[Schema]]] = []
        self.model_network = nx.Graph()

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

    def _generate_file(self, path, func: GENERATE_FUNC, **kwargs):
        content = func(**kwargs)
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

    def _get_pydantic_models(self, root=Schema):
        for model_ in root.__subclasses__():
            yield model_
            yield from self._get_pydantic_models(model_)

    def _parse_models(self):
        self.define_schemas = {m.__name__: m for m in self._get_pydantic_models()}
        self.model_render_data: Dict[str, ModelRenderData] = {
            n: ModelRenderData(name=self._name_info(n), model=m)
            for n, m in self.define_schemas.items()
        }
        for n, m in self.define_schemas.items():
            self._make_render_data(n, m, self.model_render_data)
        for a in self.model_render_data.values():
            for l1 in a.links:
                for l2 in self.model_render_data[l1.m2.name.camel].links:
                    if l2.m2.name.camel != a.name.camel:
                        continue
                    l1.t2 = l2.t1
                    l2.t2 = l1.t1
                    break

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

    def _make_render_data(self, model_name: str, model_: Type[Schema],
                          d: Dict[str, ModelRenderData]) -> ModelRenderData:
        def is_model(t: Type) -> bool:
            return isinstance(t, type) and Schema.__subclasscheck__(t)

        def is_batch_model(t: Type) -> bool:
            if hasattr(t, '__origin__') and Sequence.__subclasscheck__(
                    getattr(t, '__origin__')):
                seq_member: Type[Schema] = getattr(t, '__args__')[0]
                return is_model(seq_member)
            return False

        model = d[model_name]
        for name, field in model_.model_fields.items():
            if name in ['id']:
                raise ValueError(f'{model_name}.{name} is reserved')

            field_type: Type[Schema] | None = field.annotation
            if field_type is None:
                raise ValueError(f'{model_name}.{name} missing type hint')

            if is_model(field_type):
                model.links.append(Link(
                    t1='one', t2=None, m1=model, m2=d[field_type.__name__],
                    nullable=not field.is_required()))
                self.model_network.add_edge(model.name.camel, d[field_type.__name__].name.camel)
                continue

            if is_batch_model(field_type):
                model.links.append(Link(
                    t1="many", t2=None, m1=model, m2=d[getattr(field_type, '__args__')[0].__name__],
                    nullable=not field.is_required()))
                continue

            model.fields.append(
                {
                    'name': self._name_info(name),
                    'type': field.annotation.__name__,
                    'sql_type': 'sqltypes.' + mapping(field.annotation).__name__,
                    'default': field.default,
                    'default_factory': field.default_factory,
                    'nullable': not field.is_required(),
                    'alias': field.alias,
                }
            )
        return model

    def _define2table(self) -> str:
        template = self.env.get_template('models/main.py.jinja2')
        return template.render(models=list(filter(lambda x: x.name.camel != 'User', self.model_render_data.values())))

    def _define2schema(self) -> str:
        template = self.env.get_template('schemas/main.py.jinja2')
        return template.render(models=list(filter(lambda x: x.name.camel != 'User', self.model_render_data.values())))

    def _define2mock(self) -> str:
        raise NotImplementedError()

    def _from_template(self, template_name: str, **kwargs):
        def func():
            return self.env.get_template(template_name).render(**kwargs)

        return func

    def _generate_tables(self):
        self._generate_file(os.path.join(self.root_path, 'db.py'), self._from_template('db.py.jinja2'))
        self._generate_file(os.path.join(self.root_path, 'setting.py'), self._from_template('setting.py.jinja2'))
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

    def _generate_auth(self):
        user_model = self.model_render_data['User']
        self._generate_file(os.path.join(self.auth_path, '__init__.py'), self._from_template('auth/__init__.py.j2'))
        self._generate_file(os.path.join(self.auth_path, 'models.py'),
                            self._from_template('auth/models.py.j2', model=user_model))
        self._generate_file(os.path.join(self.auth_path, 'routes.py'), self._from_template('auth/routes.py.j2'))
        self._generate_file(os.path.join(self.auth_path, 'utils.py'), self._from_template('auth/utils.py.j2'))

    def _generate_config(self):
        self._generate_file(os.path.join(self.root_path, 'config.py'), self._from_template(
            'config.py.j2', models=self.model_render_data.values()))

    def generate(self, table: bool = True, router: bool = True, mock: bool = True, auth: bool = True):
        self.parse()
        if table:
            self._generate_tables()
        if router:
            self._generate_routers()
        if mock:
            self._generate_mock()
        if auth:
            self._generate_auth()
        self._generate_config()
