# generate_hash: 06dd92e48293e7cec34a4335af251ed9
"""
This file was automatically generated in 2024-09-06 16:25:17.799330
"""

from fastapi_toolkit.base.router import BaseRouter

from ..config import ModelConfig
from ..repo.item_repo import *


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
