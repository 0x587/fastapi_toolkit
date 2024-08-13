# generate_hash: bf773898f39a020d979e084c7350a5b9
"""
This file was automatically generated in 2024-08-14 00:21:38.644386
"""
from typing import Union

from fastapi_toolkit.define.config import ModelConfig


class Config:
    user: Union[ModelConfig, bool] = ModelConfig()
    post: Union[ModelConfig, bool] = ModelConfig()
    comment: Union[ModelConfig, bool] = ModelConfig()
    post_like: Union[ModelConfig, bool] = ModelConfig()
    comment_like: Union[ModelConfig, bool] = ModelConfig()
