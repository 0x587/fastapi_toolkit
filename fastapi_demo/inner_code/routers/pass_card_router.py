# generate_hash: f3d2df6438c7fa7cf25aad964ebe6b2f
"""
This file was automatically generated in 2024-08-18 00:30:05.042050
"""

from fastapi_toolkit.base.router import BaseRouter

from ..config import ModelConfig
from ..crud.pass_card_crud import *


class PassCardRouter(BaseRouter):
    def __init__(self, config: ModelConfig):
        self.snake_name = "pass_card"
        self.snake_plural_name = "pass_cards"
        self.camel_name = "PassCard"
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
