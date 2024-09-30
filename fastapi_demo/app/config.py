from typing import Union

from fastapi_toolkit.define.config import ModelConfig


class Config:
    user: Union[ModelConfig, bool] = ModelConfig()
    info_block: Union[ModelConfig, bool] = ModelConfig()
    certified_record: Union[ModelConfig, bool] = ModelConfig()
