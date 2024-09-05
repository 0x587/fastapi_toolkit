# generate_hash: f394dcdc148d90df5ff6559307e6246d
"""
This file was automatically generated in 2024-09-05 10:54:53.685527
"""
from functools import lru_cache
from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    host: str
    port: int
    user: str
    password: str
    database: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings():
    return Setting()


setting = get_settings()