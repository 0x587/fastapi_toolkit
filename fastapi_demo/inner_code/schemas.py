# generate_hash: 1d7abba6cf5caa11bd4e5cb0d597b479
"""
This file was automatically generated in 2024-08-18 00:30:05.034363
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
    name: str = Field()

    user_key: str = Field()


class SchemaUser(SchemaBaseUser):
    """relationships"""
    posts: "List[SchemaBasePost]"
    comments: "List[SchemaBaseComment]"
    post_likes: "List[SchemaBasePostLike]"
    comment_likes: "List[SchemaBaseCommentLike]"
    pass_card: "Optional[SchemaBasePassCard]"
    groups: "List[SchemaBaseGroup]"


class SchemaBasePassCard(Schema):
    """pk"""
    id: int = Field(default=None)

    deleted_at: Optional[datetime.datetime] = Field(default=None, exclude=True)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

    """fields"""
    account: int = Field()


class SchemaPassCard(SchemaBasePassCard):
    """relationships"""
    user: "Optional[SchemaBaseUser]"


class SchemaBaseGroup(Schema):
    """pk"""
    id: int = Field(default=None)

    deleted_at: Optional[datetime.datetime] = Field(default=None, exclude=True)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

    """fields"""
    name: str = Field()


class SchemaGroup(SchemaBaseGroup):
    """relationships"""
    users: "List[SchemaBaseUser]"


class SchemaBasePost(Schema):
    """pk"""
    id: int = Field(default=None)

    deleted_at: Optional[datetime.datetime] = Field(default=None, exclude=True)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

    """fields"""
    text: str = Field()


class SchemaPost(SchemaBasePost):
    """relationships"""
    author: "Optional[SchemaBaseUser]"
    comments: "List[SchemaBaseComment]"
    likes: "List[SchemaBasePostLike]"


class SchemaBaseComment(Schema):
    """pk"""
    id: int = Field(default=None)

    deleted_at: Optional[datetime.datetime] = Field(default=None, exclude=True)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

    """fields"""
    content: str = Field()


class SchemaComment(SchemaBaseComment):
    """relationships"""
    user: "Optional[SchemaBaseUser]"
    post: "Optional[SchemaBasePost]"
    likes: "List[SchemaBaseCommentLike]"


class SchemaBasePostLike(Schema):
    """pk"""
    id: int = Field(default=None)

    deleted_at: Optional[datetime.datetime] = Field(default=None, exclude=True)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

    """fields"""

class SchemaPostLike(SchemaBasePostLike):
    """relationships"""
    user: "Optional[SchemaBaseUser]"
    post: "Optional[SchemaBasePost]"


class SchemaBaseCommentLike(Schema):
    """pk"""
    id: int = Field(default=None)

    deleted_at: Optional[datetime.datetime] = Field(default=None, exclude=True)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

    """fields"""

class SchemaCommentLike(SchemaBaseCommentLike):
    """relationships"""
    user: "Optional[SchemaBaseUser]"
    comment: "Optional[SchemaBaseComment]"


SchemaBaseUser.model_rebuild()
SchemaUser.model_rebuild()
SchemaBasePassCard.model_rebuild()
SchemaPassCard.model_rebuild()
SchemaBaseGroup.model_rebuild()
SchemaGroup.model_rebuild()
SchemaBasePost.model_rebuild()
SchemaPost.model_rebuild()
SchemaBaseComment.model_rebuild()
SchemaComment.model_rebuild()
SchemaBasePostLike.model_rebuild()
SchemaPostLike.model_rebuild()
SchemaBaseCommentLike.model_rebuild()
SchemaCommentLike.model_rebuild()
