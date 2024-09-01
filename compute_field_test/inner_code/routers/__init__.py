# generate_hash: d64e27dcf123212dc4f27b98ca29be7e
"""
This file was automatically generated in 2024-09-01 22:59:21.239356
"""
from fastapi import APIRouter

from .user_router import UserRouter
from .item_router import ItemRouter
from .range_router import RangeRouter


class InnerRouter(APIRouter):
    def __init__(self, config):
        super().__init__()
        if not config:
            return
        if config.user:
            self.include_router(UserRouter(config.user))
        if config.item:
            self.include_router(ItemRouter(config.item))
        if config.range:
            self.include_router(RangeRouter(config.range))


__all__ = [
    'InnerRouter',
]
