# generate_hash: 841d4ca87af78c8fa25527e1a19108f5
"""
This file was automatically generated in 2024-08-14 00:21:38.642855
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
        self.add_api_route(
            endpoint=get_all_is_user_id,
            methods=["POST"],
            path='/get_all_is_user_id'
        )
        self.add_api_route(
            endpoint=get_all_is_user,
            methods=["POST"],
            path='/get_all_is_user'
        )
        self.add_api_route(
            endpoint=get_all_has_user_id,
            methods=["POST"],
            path='/get_all_has_user_id'
        )
        self.add_api_route(
            endpoint=get_all_has_user,
            methods=["POST"],
            path='/get_all_has_user'
        )
        self.add_api_route(
            endpoint=get_all_is_comment_id,
            methods=["POST"],
            path='/get_all_is_comment_id'
        )
        self.add_api_route(
            endpoint=get_all_is_comment,
            methods=["POST"],
            path='/get_all_is_comment'
        )
        self.add_api_route(
            endpoint=get_all_has_comment_id,
            methods=["POST"],
            path='/get_all_has_comment_id'
        )
        self.add_api_route(
            endpoint=get_all_has_comment,
            methods=["POST"],
            path='/get_all_has_comment'
        )

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
