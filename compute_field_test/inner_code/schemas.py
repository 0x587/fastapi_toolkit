# generate_hash: a81fe813ad549ddaaac23db796e2561c
"""
This file was automatically generated in 2024-09-01 22:59:20.605937
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
    user_key: str = Field()


class SchemaUser(SchemaBaseUser):
    """relationships"""


class SchemaBaseItem(Schema):
    """pk"""
    id: int = Field(default=None)

    deleted_at: Optional[datetime.datetime] = Field(default=None, exclude=True)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

    """fields"""
    value: int = Field()


class SchemaItem(SchemaBaseItem):
    """relationships"""


class SchemaBaseRange(Schema):
    """pk"""
    id: int = Field(default=None)

    deleted_at: Optional[datetime.datetime] = Field(default=None, exclude=True)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

    """fields"""
    min_value: int = Field()

    max_value: int = Field()


class SchemaRange(SchemaBaseRange):
    """relationships"""


SchemaBaseUser.model_rebuild()
SchemaUser.model_rebuild()
SchemaBaseItem.model_rebuild()
SchemaItem.model_rebuild()
SchemaBaseRange.model_rebuild()
SchemaRange.model_rebuild()
