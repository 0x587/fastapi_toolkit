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