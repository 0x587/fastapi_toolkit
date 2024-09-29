import models
from sqlmodel import Field, SQLModel, create_engine
from fastapi_toolkit.generate import CodeGenerator

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)

SQLModel.metadata.create_all(engine)

g = CodeGenerator()
g.parse()

g.generate_repo()
g.generate_router()
g._generate_auth('key')
g.generate_db()
g.generate_dev()
g._generate_config()