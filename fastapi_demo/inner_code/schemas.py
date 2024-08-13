# generate_hash: f983980e17bcbda7b2ceec59419e6d18
"""
This file was automatically generated in 2024-08-14 00:21:38.636293
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


class SchemaUser(SchemaBaseUser):
    """relationships"""
    posts: "List[SchemaBasePost]"
    comments: "List[SchemaBaseComment]"
    post_likes: "List[SchemaBasePostLike]"
    comment_likes: "List[SchemaBaseCommentLike]"


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
SchemaBasePost.model_rebuild()
SchemaPost.model_rebuild()
SchemaBaseComment.model_rebuild()
SchemaComment.model_rebuild()
SchemaBasePostLike.model_rebuild()
SchemaPostLike.model_rebuild()
SchemaBaseCommentLike.model_rebuild()
SchemaCommentLike.model_rebuild()
