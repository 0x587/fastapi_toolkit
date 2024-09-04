# generate_hash: 5f742a55c011593142efc0155f36fbfd
"""
This file was automatically generated in 2024-09-04 15:14:00.246821
"""

from fastapi_toolkit.base.router import BaseRouter

from ..config import ModelConfig
from ..crud.range_crud import *


class RangeRouter(BaseRouter):
    def __init__(self, config: ModelConfig):
        self.snake_name = "range"
        self.snake_plural_name = "ranges"
        self.camel_name = "Range"
        super().__init__(config)

    def _get_one(self):
        return get_one

    def _batch_get(self):
        return batch_get

    def _get_all(self):
        return get_all

    def _get_link_all(self):
        return get_link_all

    def _create_one(self):
        return create_one

    def _update_one(self):
        return update_one

    def _delete_one(self):
        return delete_one
