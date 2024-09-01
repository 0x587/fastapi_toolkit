# generate_hash: 6463a04576f7410b38c79b864a716efc
"""
This file was automatically generated in 2024-09-01 22:59:02.271593
"""
from inner_code.setting import get_settings

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
    user = setting.user
    password = setting.password
    host = setting.host
    db_name = setting.database

    config = configparser.ConfigParser()
    config.read(alembic_ini_path)
    config["alembic"]["sqlalchemy.url"] = f"mysql+pymysql://{user}:{password}@{host}/{db_name}"
    with open(alembic_ini_path, "w") as f:
        config.write(f)

    with open(".alembic/env.py", "r") as f:
        env_content = f.read()
        env_content = ("from sqlalchemy.orm import DeclarativeBase\n"
                       f"from inner_code.models import *\n"
                       f"from inner_code.auth.models import *\n") + env_content
        env_content = env_content.replace("target_metadata = None",
                                          "target_metadata = Base.metadata")
    with open(".alembic/env.py", "w") as f:
        f.write(env_content)


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