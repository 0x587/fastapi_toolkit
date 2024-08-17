# generate_hash: 5ea2d3b03baf2670d407bdfe47b68315
"""
This file was automatically generated in 2024-08-18 00:30:05.042277
"""

from fastapi_toolkit.base.router import BaseRouter

from ..config import ModelConfig
from ..crud.group_crud import *


class GroupRouter(BaseRouter):
    def __init__(self, config: ModelConfig):
        self.snake_name = "group"
        self.snake_plural_name = "groups"
        self.camel_name = "Group"
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
