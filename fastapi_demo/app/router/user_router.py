# generate_hash: 1903d9997b950c81f5adecda9f366483
"""
This file was automatically generated in 2024-09-29 00:28:32.162492
"""

from fastapi_toolkit.base.router import BaseRouter

from ..config import ModelConfig
from ..repo.user_repo import *


class UserRouter(BaseRouter):
    def __init__(self, config: ModelConfig):
        self.snake_name = "user"
        self.snake_plural_name = "users"
        self.camel_name = "User"
        super().__init__(config, User)

    def _get_one(self):
        return get_one

    def _batch_get(self):
        return batch_get

    def _get_all(self):
        return get_all

    def _create_one(self):
        return create_one

    def _update_one(self):
        return update_one

    def _delete_one(self):
        return delete_one
