# generate_hash: 9934b2f954ad6aa863627d54d4c99152
"""
This file was automatically generated in 2024-10-10 15:04:55.288891
"""

from fastapi_toolkit.base.router import BaseRouter

from ..config import ModelConfig
from ..repo.user_repo import *


class UserRouter(BaseRouter):
    def __init__(self, config: ModelConfig):
        self.snake_name = "user"
        self.snake_plural_name = "users"
        self.camel_name = "User"
        super().__init__(config, SchemaBaseUser, SchemaUser)

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
