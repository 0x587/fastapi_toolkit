# generate_hash: 92642379516a06de838b7df749c106f4
"""
This file was automatically generated in 2024-09-04 15:14:00.244958
"""

from fastapi_toolkit.base.router import BaseRouter

from ..config import ModelConfig
from ..crud.user_crud import *


class UserRouter(BaseRouter):
    def __init__(self, config: ModelConfig):
        self.snake_name = "user"
        self.snake_plural_name = "users"
        self.camel_name = "User"
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
