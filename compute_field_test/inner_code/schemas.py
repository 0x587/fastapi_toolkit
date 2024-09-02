# generate_hash: 42818ae20fcbd0eca28d416f1d50f802
"""
This file was automatically generated in 2024-09-02 19:04:05.899622
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
    user_key: str = Field()


class SchemaUser(SchemaBaseUser):
    """relationships"""


class UserSession(SchemaUser):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    db: Session = Field(exclude=True)


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


class ItemSession(SchemaItem):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    db: Session = Field(exclude=True)


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


class RangeSession(SchemaRange):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    db: Session = Field(exclude=True)


SchemaBaseUser.model_rebuild()
SchemaUser.model_rebuild()
SchemaBaseItem.model_rebuild()
SchemaItem.model_rebuild()
SchemaBaseRange.model_rebuild()
SchemaRange.model_rebuild()
