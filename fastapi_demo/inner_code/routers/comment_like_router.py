# generate_hash: 530e523e34c60941ff22e38a1f25339b
"""
This file was automatically generated in 2024-08-15 16:29:03.786786
"""

from fastapi_toolkit.base.router import BaseRouter

from ..config import ModelConfig
from ..crud.comment_like_crud import *


class CommentLikeRouter(BaseRouter):
    def __init__(self, config: ModelConfig):
        self.snake_name = "comment_like"
        self.snake_plural_name = "comment_likes"
        self.camel_name = "CommentLike"
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
