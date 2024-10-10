# generate_hash: 1b8282416da50dce3bc1b320f8dd05cf
"""
This file was automatically generated in 2024-10-10 15:06:33.646480
"""
import uuid
import datetime
from typing import List, Optional

from fastapi_toolkit.define import Schema
from pydantic import Field


class SchemaBaseUser(Schema):
    """pk"""
    id: int = Field(default=None)

    deleted_at: Optional[datetime.datetime] = Field(default=None, exclude=True)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

    """fields"""
    sex: bool = Field(
    )
    title: str = Field(
    )
    name: str = Field(
    )
    desc: str = Field(
    )
    bg_img: str = Field(
    )
    hot_level: int = Field(
    )
    star_level: int = Field(
    )
    user_key: str = Field(
    )
    avatar: Optional[str] = Field(
        default=None
    )


class SchemaUser(SchemaBaseUser):
    """relationships"""
    info_blocks: "List[SchemaBaseInfoBlock]" = Field(default_factory=list)
    certified_records: "List[SchemaBaseCertifiedRecord]" = Field(default_factory=list)


class SchemaBaseInfoBlock(Schema):
    """pk"""
    id: int = Field(default=None)

    deleted_at: Optional[datetime.datetime] = Field(default=None, exclude=True)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

    """fields"""
    type: str = Field(
    )
    title: str = Field(
    )
    sub_title: str = Field(
    )
    desc: str = Field(
    )
    tags: str = Field(
    )
    time_start: datetime.date = Field(
    )
    time_end: datetime.date = Field(
    )
    show: bool = Field(
        default=False
    )


class SchemaInfoBlock(SchemaBaseInfoBlock):
    """relationships"""
    user: "Optional[SchemaBaseUser]" = None
    certified_records: "List[SchemaBaseCertifiedRecord]" = Field(default_factory=list)


class SchemaBaseCertifiedRecord(Schema):
    """pk"""
    id: int = Field(default=None)

    deleted_at: Optional[datetime.datetime] = Field(default=None, exclude=True)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

    """fields"""
    done: bool = Field(
    )
    target_real_name: str = Field(
    )
    self_real_name: str = Field(
    )
    relation: str = Field(
    )


class SchemaCertifiedRecord(SchemaBaseCertifiedRecord):
    """relationships"""
    user: "Optional[SchemaBaseUser]" = None
    info_block: "Optional[SchemaBaseInfoBlock]" = None


SchemaBaseUser.model_rebuild()
SchemaUser.model_rebuild()
SchemaBaseInfoBlock.model_rebuild()
SchemaInfoBlock.model_rebuild()
SchemaBaseCertifiedRecord.model_rebuild()
SchemaCertifiedRecord.model_rebuild()

__all__ = [
    'SchemaBaseUser',
    'SchemaUser',
    'SchemaBaseInfoBlock',
    'SchemaInfoBlock',
    'SchemaBaseCertifiedRecord',
    'SchemaCertifiedRecord',
]