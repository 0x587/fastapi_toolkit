# generate_hash: 7627b51b01142401b6cde4d3218930a6
"""
This file was automatically generated in 2024-09-29 11:10:40.292053
"""
from fastapi import APIRouter

from .user_router import UserRouter
from .info_block_router import InfoBlockRouter
from .certified_record_router import CertifiedRecordRouter


class InnerRouter(APIRouter):
    def __init__(self, config):
        super().__init__()
        if not config:
            return
        if config.user:
            self.include_router(UserRouter(config.user))
        if config.info_block:
            self.include_router(InfoBlockRouter(config.info_block))
        if config.certified_record:
            self.include_router(CertifiedRecordRouter(config.certified_record))


__all__ = [
    'InnerRouter',
]
