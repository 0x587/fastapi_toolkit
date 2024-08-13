# generate_hash: 9352781531fb40acb892dca9e91a7b5a
"""
This file was automatically generated in 2024-08-14 00:21:38.643786
"""
from fastapi import APIRouter

from .user_router import UserRouter
from .post_router import PostRouter
from .comment_router import CommentRouter
from .post_like_router import PostLikeRouter
from .comment_like_router import CommentLikeRouter


class InnerRouter(APIRouter):
    def __init__(self, config):
        super().__init__()
        if not config:
            return
        if config.user:
            self.include_router(UserRouter(config.user))
        if config.post:
            self.include_router(PostRouter(config.post))
        if config.comment:
            self.include_router(CommentRouter(config.comment))
        if config.post_like:
            self.include_router(PostLikeRouter(config.post_like))
        if config.comment_like:
            self.include_router(CommentLikeRouter(config.comment_like))


__all__ = [
    'InnerRouter',
]
