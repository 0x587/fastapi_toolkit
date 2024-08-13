# generate_hash: bca17ad70ae44c488a49eb37cb728da2
"""
This file was automatically generated in 2024-08-14 00:21:38.642674
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
            endpoint=get_all_is_post_id,
            methods=["POST"],
            path='/get_all_is_post_id'
        )
        self.add_api_route(
            endpoint=get_all_is_post,
            methods=["POST"],
            path='/get_all_is_post'
        )
        self.add_api_route(
            endpoint=get_all_has_post_id,
            methods=["POST"],
            path='/get_all_has_post_id'
        )
        self.add_api_route(
            endpoint=get_all_has_post,
            methods=["POST"],
            path='/get_all_has_post'
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
