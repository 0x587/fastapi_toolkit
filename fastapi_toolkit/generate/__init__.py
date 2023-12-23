import datetime
import os
import hashlib
import typer
from typing import Callable, Any, Sequence, Dict, List, Optional, Tuple, Literal, Type
from jinja2 import Environment, PackageLoader

from pydantic import BaseModel as PydanticBaseModel
from fastapi_toolkit.define import BaseModel

from .sql_mapping import mapping
from .utils import to_snake, plural

GENERATE_FUNC = Callable[[Any, ...], str]


class NameInfo(PydanticBaseModel):
    snake: str
    snake_plural: str
    camel: str
    camel_plural: str
    table: str
    db: str
    schema: str
    base_schema: str
    fk: str


class Link(PydanticBaseModel):
    t1: Literal["one", "many"]
    t2: Optional[Literal["one", "many"]]
    m1: 'ModelRenderData'
    m2: 'ModelRenderData'
    nullable: bool


class ModelRenderData(PydanticBaseModel):
    name: NameInfo
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

        self.models: Dict[str, Type[BaseModel]] = {}
        self.links: List[Tuple[Literal["one"] | Literal["many"], Type[BaseModel], Type[BaseModel]]] = []

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

    def _get_pydantic_models(self, root=BaseModel):
        for model_ in root.__subclasses__():
            yield model_
            yield from self._get_pydantic_models(model_)

    def _parse_models(self):
        self.models = {m.__name__: m for m in self._get_pydantic_models()}
        self.model_render_data = {}
        for n, m in self.models.items():
            self.model_render_data[n] = ModelRenderData(name=self._name_info(n))
        for n, m in self.models.items():
            self._make_render_data(n, m)
        for a in self.model_render_data.values():
            if not a.links:
                continue
            for l1 in a.links:
                for l2 in self.model_render_data[l1.m2.name.camel].links:
                    if l2.m2.name.camel == a.name.camel:
                        l1.t2 = l2.t1
                        l2.t2 = l1.t1
                        break

    def _parse_mock(self):
        pass

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

    def _make_render_data(self, model_name: str, m: Type[BaseModel]) -> ModelRenderData:
        def is_model(t: Type) -> bool:
            return isinstance(t, type) and BaseModel.__subclasscheck__(t)

        model = self.model_render_data[model_name]
        for name, field in m.model_fields.items():
            if name in ['id']:
                raise ValueError(f'{model_name}.{name} is reserved')

            field_type: Type[BaseModel] | None = field.annotation
            if field_type is None:
                raise ValueError(f'{model_name}.{name} missing type hint')

            if is_model(field.annotation):
                model.links.append(Link(
                    t1='one', t2=None, m1=model, m2=self.model_render_data[field_type.__name__],
                    nullable=not field.is_required()))
                continue

            # is a sequence
            if hasattr(field.annotation, '__origin__') and Sequence.__subclasscheck__(
                    getattr(field.annotation, '__origin__')):
                # is a model sequence
                seq_member: Type[BaseModel] = getattr(field.annotation, '__args__')[0]
                if is_model(seq_member):
                    model.links.append(Link(
                        t1="many", t2=None, m1=model, m2=self.model_render_data[seq_member.__name__],
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

    def _router_init(self) -> str:
        return self.env.get_template('router_init.py.jinja2').render(
            models=list(filter(lambda x: x.name.camel != 'User', self.model_render_data.values())))

    def _define2mock(self) -> str:
        raise NotImplementedError()

    def _from_template(self, template_name: str, **kwargs):
        def func():
            return self.env.get_template(template_name).render(**kwargs)

        return func

    def generate_tables(self):
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

    def generate_routers(self):
        for model in self.model_render_data.values():
            if model.name.camel == 'User':
                continue
            self._generate_file(os.path.join(self.crud_path, f'{model.name.snake}_crud.py'),
                                self._from_template('crud/main.py.jinja2', model=model))
            self._generate_file(os.path.join(self.routers_path, f'{model.name.snake}_router.py'),
                                self._from_template('router.py.jinja2', model=model))
        self._generate_file(os.path.join(self.routers_path, '__init__.py'), self._router_init)
        self._generate_file(os.path.join(self.crud_path, '__init__.py'), lambda: '')

    def generate_mock(self):
        raise NotImplementedError()

    def generate_auth(self):
        user_model = self._make_render_data('User', self.models['User'])
        self._generate_file(os.path.join(self.auth_path, '__init__.py'), self._from_template('auth/__init__.py.j2'))
        self._generate_file(os.path.join(self.auth_path, 'models.py'),
                            self._from_template('auth/models.py.j2', model=user_model))
        self._generate_file(os.path.join(self.auth_path, 'routes.py'), self._from_template('auth/routes.py.j2'))
        self._generate_file(os.path.join(self.auth_path, 'utils.py'), self._from_template('auth/utils.py.j2'))
