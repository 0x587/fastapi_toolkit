# generate_hash: 018bf5889e4654dd861968d8ed0ea210
"""
This file was automatically generated in 2024-08-15 16:29:03.784419
"""

from fastapi_toolkit.base.router import BaseRouter

from ..config import ModelConfig
from ..crud.post_crud import *


class PostRouter(BaseRouter):
    def __init__(self, config: ModelConfig):
        self.snake_name = "post"
        self.snake_plural_name = "posts"
        self.camel_name = "Post"
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
