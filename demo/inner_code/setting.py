# generate_hash: 1c0e484c963177a34a7dee4361f7c526
"""
This file was automatically generated in 2024-08-06 22:49:59.053322
"""
from functools import lru_cache
from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    host: str
    port: int
    user: str
    password: str
    database: str

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings():
    return Setting()


setting = get_settings()