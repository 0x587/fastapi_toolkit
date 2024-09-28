# generate_hash: 5afa6d2cc6a1959e851a96e5bb7fa21c
"""
This file was automatically generated in 2024-09-29 00:28:32.165744
"""
from functools import lru_cache
from pydantic import Field
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