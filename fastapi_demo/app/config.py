# generate_hash: 63b724fb910a0eff71e3348c1b01e3f8
"""
This file was automatically generated in 2024-09-29 11:10:40.300477
"""
from typing import Union

from fastapi_toolkit.define.config import ModelConfig


class Config:
    user: Union[ModelConfig, bool] = ModelConfig()
    info_block: Union[ModelConfig, bool] = ModelConfig()
    certified_record: Union[ModelConfig, bool] = ModelConfig()
