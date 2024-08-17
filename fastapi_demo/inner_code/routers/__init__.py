# generate_hash: 16c7ba95fccf42750575189cc7702f0d
"""
This file was automatically generated in 2024-08-18 00:30:05.044503
"""
from fastapi import APIRouter

from .user_router import UserRouter
from .pass_card_router import PassCardRouter
from .group_router import GroupRouter
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
        if config.pass_card:
            self.include_router(PassCardRouter(config.pass_card))
        if config.group:
            self.include_router(GroupRouter(config.group))
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
