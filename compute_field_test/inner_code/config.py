# generate_hash: 6193e08461840f3d124ddf9d587076cf
"""
This file was automatically generated in 2024-09-01 22:59:21.245310
"""
from typing import Union

from fastapi_toolkit.define.config import ModelConfig


class Config:
    user: Union[ModelConfig, bool] = ModelConfig()
    item: Union[ModelConfig, bool] = ModelConfig()
    range: Union[ModelConfig, bool] = ModelConfig()
