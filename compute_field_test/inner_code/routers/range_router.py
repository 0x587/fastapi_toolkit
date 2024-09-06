# generate_hash: 0b5b2901cb3891312b56f91f3f7e5bd8
"""
This file was automatically generated in 2024-09-06 16:25:17.800434
"""

from fastapi_toolkit.base.router import BaseRouter

from ..config import ModelConfig
from ..repo.range_repo import *


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
