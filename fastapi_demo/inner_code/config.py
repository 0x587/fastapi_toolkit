# generate_hash: d93a02e78ce6fb2f5b38149185bc0a2d
"""
This file was automatically generated in 2024-08-18 00:30:05.047420
"""
from typing import Union

from fastapi_toolkit.define.config import ModelConfig


class Config:
    user: Union[ModelConfig, bool] = ModelConfig()
    pass_card: Union[ModelConfig, bool] = ModelConfig()
    group: Union[ModelConfig, bool] = ModelConfig()
    post: Union[ModelConfig, bool] = ModelConfig()
    comment: Union[ModelConfig, bool] = ModelConfig()
    post_like: Union[ModelConfig, bool] = ModelConfig()
    comment_like: Union[ModelConfig, bool] = ModelConfig()
