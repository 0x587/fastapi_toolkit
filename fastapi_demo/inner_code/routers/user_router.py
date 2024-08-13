# generate_hash: d6d174bbe9c6d6715b3d39bde7d247c9
"""
This file was automatically generated in 2024-08-14 00:21:38.641956
"""

from fastapi_toolkit.base.router import BaseRouter

from ..config import ModelConfig
from ..crud.user_crud import *


class UserRouter(BaseRouter):
    def __init__(self, config: ModelConfig):
        self.snake_name = "user"
        self.snake_plural_name = "users"
        self.camel_name = "User"
        super().__init__(config)
        self.add_api_route(
            endpoint=get_all_is_posts_id,
            methods=["POST"],
            path='/get_all_is_posts_id'
        )
        self.add_api_route(
            endpoint=get_all_is_posts,
            methods=["POST"],
            path='/get_all_is_posts'
        )
        self.add_api_route(
            endpoint=get_all_has_posts_id,
            methods=["POST"],
            path='/get_all_has_posts_id'
        )
        self.add_api_route(
            endpoint=get_all_has_posts,
            methods=["POST"],
            path='/get_all_has_posts'
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
            endpoint=get_all_is_post_likes_id,
            methods=["POST"],
            path='/get_all_is_post_likes_id'
        )
        self.add_api_route(
            endpoint=get_all_is_post_likes,
            methods=["POST"],
            path='/get_all_is_post_likes'
        )
        self.add_api_route(
            endpoint=get_all_has_post_likes_id,
            methods=["POST"],
            path='/get_all_has_post_likes_id'
        )
        self.add_api_route(
            endpoint=get_all_has_post_likes,
            methods=["POST"],
            path='/get_all_has_post_likes'
        )
        self.add_api_route(
            endpoint=get_all_is_comment_likes_id,
            methods=["POST"],
            path='/get_all_is_comment_likes_id'
        )
        self.add_api_route(
            endpoint=get_all_is_comment_likes,
            methods=["POST"],
            path='/get_all_is_comment_likes'
        )
        self.add_api_route(
            endpoint=get_all_has_comment_likes_id,
            methods=["POST"],
            path='/get_all_has_comment_likes_id'
        )
        self.add_api_route(
            endpoint=get_all_has_comment_likes,
            methods=["POST"],
            path='/get_all_has_comment_likes'
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
