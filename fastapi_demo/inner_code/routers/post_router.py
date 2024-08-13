# generate_hash: b9b52bffb7da593a7e2c4adbdb789c83
"""
This file was automatically generated in 2024-08-14 00:21:38.642231
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
        self.add_api_route(
            endpoint=get_all_is_author_id,
            methods=["POST"],
            path='/get_all_is_author_id'
        )
        self.add_api_route(
            endpoint=get_all_is_author,
            methods=["POST"],
            path='/get_all_is_author'
        )
        self.add_api_route(
            endpoint=get_all_has_author_id,
            methods=["POST"],
            path='/get_all_has_author_id'
        )
        self.add_api_route(
            endpoint=get_all_has_author,
            methods=["POST"],
            path='/get_all_has_author'
        )
        self.add_api_route(
            endpoint=get_all_is_comments_id,
            methods=["POST"],
            path='/get_all_is_comments_id'
        )
        self.add_api_route(
            endpoint=get_all_is_comments,
            methods=["POST"],
            path='/get_all_is_comments'
        )
        self.add_api_route(
            endpoint=get_all_has_comments_id,
            methods=["POST"],
            path='/get_all_has_comments_id'
        )
        self.add_api_route(
            endpoint=get_all_has_comments,
            methods=["POST"],
            path='/get_all_has_comments'
        )
        self.add_api_route(
            endpoint=get_all_is_likes_id,
            methods=["POST"],
            path='/get_all_is_likes_id'
        )
        self.add_api_route(
            endpoint=get_all_is_likes,
            methods=["POST"],
            path='/get_all_is_likes'
        )
        self.add_api_route(
            endpoint=get_all_has_likes_id,
            methods=["POST"],
            path='/get_all_has_likes_id'
        )
        self.add_api_route(
            endpoint=get_all_has_likes,
            methods=["POST"],
            path='/get_all_has_likes'
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
