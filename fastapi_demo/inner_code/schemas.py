# generate_hash: 62f6620f96fcc4efa256e2f2945a7da2
"""
This file was automatically generated in 2024-09-02 19:03:29.861698
"""
import uuid
import datetime
from typing import List, Optional

from fastapi_toolkit.define import Schema
from pydantic import Field, ConfigDict
from sqlalchemy.orm import Session



class SchemaBaseUser(Schema):
    """pk"""
    id: int = Field(default=None)

    deleted_at: Optional[datetime.datetime] = Field(default=None, exclude=True)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

    """fields"""
    sex: bool = Field()

    title: str = Field()

    name: str = Field()

    desc: str = Field()

    avatar: str = Field()

    bg_img: str = Field()

    hot_level: int = Field()

    star_level: int = Field()

    user_key: str = Field()


class SchemaUser(SchemaBaseUser):
    """relationships"""
    info_blocks: "List[SchemaBaseInfoBlock]" = Field(default_factory=list)
    certified_records: "List[SchemaBaseCertifiedRecord]" = Field(default_factory=list)


class UserSession(SchemaUser):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    db: Session = Field(exclude=True)


class SchemaBaseInfoBlock(Schema):
    """pk"""
    id: int = Field(default=None)

    deleted_at: Optional[datetime.datetime] = Field(default=None, exclude=True)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

    """fields"""
    type: str = Field()

    title: str = Field()

    sub_title: str = Field()

    desc: str = Field()

    tags: str = Field()

    show: bool = Field()

    time_start: datetime.date = Field()

    time_end: datetime.date = Field()


class SchemaInfoBlock(SchemaBaseInfoBlock):
    """relationships"""
    user: "Optional[SchemaBaseUser]" = None
    certified_records: "List[SchemaBaseCertifiedRecord]" = Field(default_factory=list)


class InfoBlockSession(SchemaInfoBlock):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    db: Session = Field(exclude=True)


class SchemaBaseCertifiedRecord(Schema):
    """pk"""
    id: int = Field(default=None)

    deleted_at: Optional[datetime.datetime] = Field(default=None, exclude=True)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

    """fields"""
    done: bool = Field()

    target_real_name: str = Field()

    self_real_name: str = Field()

    relation: str = Field()


class SchemaCertifiedRecord(SchemaBaseCertifiedRecord):
    """relationships"""
    user: "Optional[SchemaBaseUser]" = None
    info_block: "Optional[SchemaBaseInfoBlock]" = None


class CertifiedRecordSession(SchemaCertifiedRecord):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    db: Session = Field(exclude=True)


SchemaBaseUser.model_rebuild()
SchemaUser.model_rebuild()
SchemaBaseInfoBlock.model_rebuild()
SchemaInfoBlock.model_rebuild()
SchemaBaseCertifiedRecord.model_rebuild()
SchemaCertifiedRecord.model_rebuild()
