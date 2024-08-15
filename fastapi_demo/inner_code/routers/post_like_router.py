# generate_hash: e20f419b542b0a15ccf96ce5a92c86e3
"""
This file was automatically generated in 2024-08-15 16:29:03.785812
"""

from fastapi_toolkit.base.router import BaseRouter

from ..config import ModelConfig
from ..crud.post_like_crud import *


class PostLikeRouter(BaseRouter):
    def __init__(self, config: ModelConfig):
        self.snake_name = "post_like"
        self.snake_plural_name = "post_likes"
        self.camel_name = "PostLike"
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
