# generate_hash: 0e5d98df5de73f209975c89c51ee7dd9
"""
This file was automatically generated in 2024-09-05 20:52:50.432886
"""
from functools import lru_cache
from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    host: str = Field(alias='MYSQL_ADDRESS')
    username: str = Field(alias='MYSQL_USERNAME')
    password: str = Field(alias='MYSQL_PASSWORD')
    database: str = Field(alias='MYSQL_DATABASE')

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings():
    return Setting()


setting = get_settings()