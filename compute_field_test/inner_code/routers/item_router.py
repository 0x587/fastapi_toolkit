# generate_hash: 1ad3f3e1d8bb65162e7732bc8f0c8681
"""
This file was automatically generated in 2024-09-01 22:59:02.276499
"""

from fastapi_toolkit.base.router import BaseRouter

from ..config import ModelConfig
from ..crud.item_crud import *


class ItemRouter(BaseRouter):
    def __init__(self, config: ModelConfig):
        self.snake_name = "item"
        self.snake_plural_name = "items"
        self.camel_name = "Item"
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
