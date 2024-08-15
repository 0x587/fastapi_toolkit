# generate_hash: 4cdaf130a6a917e4046cee6647a846f6
"""
This file was automatically generated in 2024-08-15 16:29:03.785135
"""

from fastapi_toolkit.base.router import BaseRouter

from ..config import ModelConfig
from ..crud.comment_crud import *


class CommentRouter(BaseRouter):
    def __init__(self, config: ModelConfig):
        self.snake_name = "comment"
        self.snake_plural_name = "comments"
        self.camel_name = "Comment"
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
