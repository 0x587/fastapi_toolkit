# generate_hash: 801c27cfae12a4660881ec20b0ab9f51
"""
This file was automatically generated in 2024-09-29 11:10:40.298569
"""
from app.setting import get_settings

"""
Database migration tool
db.py init init alembic
db.py migrate -m "init" generate migration script
db.py upgrade upgrade database
"""

import os
import re

from alembic.config import Config
from alembic import command
import configparser
import yaml
import argparse

alembic_ini_path = "./alembic.ini"


def get_app_config():
    with open("config.yaml", "r") as f:
        config_data = yaml.safe_load(f)
    return config_data


def init():
    alembic_cfg = Config(alembic_ini_path)

    command.init(alembic_cfg, "./.alembic")

    setting = get_settings()
    username = setting.username
    password = setting.password
    host = setting.host
    db_name = setting.database

    config = configparser.ConfigParser()
    config.read(alembic_ini_path)
    config["alembic"]["sqlalchemy.url"] = f"mysql+pymysql://{username}:{password}@{host}/{db_name}"
    with open(alembic_ini_path, "w") as f:
        config.write(f)

    with open(".alembic/env.py", "r") as f:
        env_content = f.read()
        env_content = ("from sqlmodel import SQLModel\n"
                       f"from app.models import *\n") + env_content
        env_content = env_content.replace("target_metadata = None",
                                          "target_metadata = SQLModel.metadata")
    with open(".alembic/env.py", "w") as f:
        f.write(env_content)

    with open(".alembic/script.py.mako", "r") as f:
        mako = f.read()
        mako = mako.replace("import sqlalchemy as sa",
                            "import sqlalchemy as sa\nimport sqlmodel")
    with open(".alembic/script.py.mako", "w") as f:
        f.write(mako)


def migrate(msg: str = None):
    if not os.path.isdir(".alembic"):
        raise Exception("alembic not init")

    alembic_cfg = Config(alembic_ini_path)
    command.revision(alembic_cfg, autogenerate=True, message=msg)


def upgrade():
    if not os.path.isdir(".alembic"):
        raise Exception("alembic not init")

    alembic_cfg = Config(alembic_ini_path)
    command.upgrade(alembic_cfg, "head")


def main():
    parser = argparse.ArgumentParser(description='Database migration')
    parser.add_argument('command', type=str, help='init, migrate, upgrade')
    parser.add_argument('--msg', '-m', type=str)
    args = parser.parse_args()
    match args.command:
        case "init":
            init()
        case "migrate":
            migrate(args.msg)
        case "upgrade":
            upgrade()


if __name__ == "__main__":
    main()