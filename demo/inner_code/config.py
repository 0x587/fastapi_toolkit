# generate_hash: ba73f0c25a420562506e85d649443bc1
"""
This file was automatically generated in 2024-08-06 22:49:59.087624
"""
from typing import Union

from fastapi_toolkit.define.config import ModelConfig


class Config:
    user: Union[ModelConfig, bool] = ModelConfig()
    department: Union[ModelConfig, bool] = ModelConfig()
    student: Union[ModelConfig, bool] = ModelConfig()
    course: Union[ModelConfig, bool] = ModelConfig()
    teacher: Union[ModelConfig, bool] = ModelConfig()
    grade: Union[ModelConfig, bool] = ModelConfig()
