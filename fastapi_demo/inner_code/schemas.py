# generate_hash: ac31764e076bd0e6844a251dd4168cb9
"""
This file was automatically generated in 2024-08-19 17:09:23.583329
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
    posts: "List[SchemaBasePost]" = Field(default=list)
    comments: "List[SchemaBaseComment]" = Field(default=list)
    post_likes: "List[SchemaBasePostLike]" = Field(default=list)
    comment_likes: "List[SchemaBaseCommentLike]" = Field(default=list)
    pass_card: "Optional[SchemaBasePassCard]" = None
    groups: "List[SchemaBaseGroup]" = Field(default=list)


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
    user: "Optional[SchemaBaseUser]" = None


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
    users: "List[SchemaBaseUser]" = Field(default=list)


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
    author: "Optional[SchemaBaseUser]" = None
    comments: "List[SchemaBaseComment]" = Field(default=list)
    likes: "List[SchemaBasePostLike]" = Field(default=list)


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
    user: "Optional[SchemaBaseUser]" = None
    post: "Optional[SchemaBasePost]" = None
    likes: "List[SchemaBaseCommentLike]" = Field(default=list)


class SchemaBasePostLike(Schema):
    """pk"""
    id: int = Field(default=None)

    deleted_at: Optional[datetime.datetime] = Field(default=None, exclude=True)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

    """fields"""

class SchemaPostLike(SchemaBasePostLike):
    """relationships"""
    user: "Optional[SchemaBaseUser]" = None
    post: "Optional[SchemaBasePost]" = None


class SchemaBaseCommentLike(Schema):
    """pk"""
    id: int = Field(default=None)

    deleted_at: Optional[datetime.datetime] = Field(default=None, exclude=True)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

    """fields"""

class SchemaCommentLike(SchemaBaseCommentLike):
    """relationships"""
    user: "Optional[SchemaBaseUser]" = None
    comment: "Optional[SchemaBaseComment]" = None


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
