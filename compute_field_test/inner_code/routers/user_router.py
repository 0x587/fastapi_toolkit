# generate_hash: d17246077a9078b6e3512c0c35f312aa
"""
This file was automatically generated in 2024-09-06 16:25:17.798166
"""

from fastapi_toolkit.base.router import BaseRouter

from ..config import ModelConfig
from ..repo.user_repo import *


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
