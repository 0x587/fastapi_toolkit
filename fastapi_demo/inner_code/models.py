# generate_hash: 59078b8f889971cfba84af3481c2e5a3
"""
This file was automatically generated in 2024-08-18 00:30:05.031883
"""
import datetime
from typing import List, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.sql import sqltypes

from .db import Base

association_table_user_group = Table(
    "association_table_user_group",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("group_id", ForeignKey("group.id"), primary_key=True),
)


class DBUser(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(sqltypes.Integer, primary_key=True, autoincrement=True)
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(sqltypes.DateTime, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(sqltypes.DateTime)
    updated_at: Mapped[datetime.datetime] = mapped_column(sqltypes.DateTime)

    name: Mapped[str] = mapped_column(sqltypes.Text, nullable=False)

    user_key: Mapped[str] = mapped_column(sqltypes.Text, nullable=False)

    posts: Mapped[List["DBPost"]] = relationship(
        back_populates="author",
    )

    comments: Mapped[List["DBComment"]] = relationship(
        back_populates="user",
    )

    post_likes: Mapped[List["DBPostLike"]] = relationship(
        back_populates="user",
    )

    comment_likes: Mapped[List["DBCommentLike"]] = relationship(
        back_populates="user",
    )

    _fk_pass_card_pass_card_id: Mapped[int] = mapped_column(ForeignKey("pass_card.id"), nullable=True)

    pass_card: Mapped[Optional["DBPassCard"]] = relationship(
        back_populates="user",
    )

    groups: Mapped[List["DBGroup"]] = relationship(
        back_populates="users",
        secondary=association_table_user_group
    )


class DBPassCard(Base):
    __tablename__ = "pass_card"

    id: Mapped[int] = mapped_column(sqltypes.Integer, primary_key=True, autoincrement=True)
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(sqltypes.DateTime, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(sqltypes.DateTime)
    updated_at: Mapped[datetime.datetime] = mapped_column(sqltypes.DateTime)

    account: Mapped[int] = mapped_column(sqltypes.Integer, nullable=False)

    user: Mapped[Optional["DBUser"]] = relationship(
        back_populates="pass_card",
    )


class DBGroup(Base):
    __tablename__ = "group"

    id: Mapped[int] = mapped_column(sqltypes.Integer, primary_key=True, autoincrement=True)
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(sqltypes.DateTime, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(sqltypes.DateTime)
    updated_at: Mapped[datetime.datetime] = mapped_column(sqltypes.DateTime)

    name: Mapped[str] = mapped_column(sqltypes.Text, nullable=False)

    users: Mapped[List["DBUser"]] = relationship(
        back_populates="groups",
        secondary=association_table_user_group
    )


class DBPost(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(sqltypes.Integer, primary_key=True, autoincrement=True)
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(sqltypes.DateTime, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(sqltypes.DateTime)
    updated_at: Mapped[datetime.datetime] = mapped_column(sqltypes.DateTime)

    text: Mapped[str] = mapped_column(sqltypes.Text, nullable=False)

    _fk_author_user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)

    author: Mapped[Optional["DBUser"]] = relationship(
        back_populates="posts",
    )

    comments: Mapped[List["DBComment"]] = relationship(
        back_populates="post",
    )

    likes: Mapped[List["DBPostLike"]] = relationship(
        back_populates="post",
    )


class DBComment(Base):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(sqltypes.Integer, primary_key=True, autoincrement=True)
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(sqltypes.DateTime, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(sqltypes.DateTime)
    updated_at: Mapped[datetime.datetime] = mapped_column(sqltypes.DateTime)

    content: Mapped[str] = mapped_column(sqltypes.Text, nullable=False)

    _fk_user_user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)

    user: Mapped[Optional["DBUser"]] = relationship(
        back_populates="comments",
    )

    _fk_post_post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=True)

    post: Mapped[Optional["DBPost"]] = relationship(
        back_populates="comments",
    )

    likes: Mapped[List["DBCommentLike"]] = relationship(
        back_populates="comment",
    )


class DBPostLike(Base):
    __tablename__ = "post_like"

    id: Mapped[int] = mapped_column(sqltypes.Integer, primary_key=True, autoincrement=True)
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(sqltypes.DateTime, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(sqltypes.DateTime)
    updated_at: Mapped[datetime.datetime] = mapped_column(sqltypes.DateTime)

    _fk_user_user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)

    user: Mapped[Optional["DBUser"]] = relationship(
        back_populates="post_likes",
    )

    _fk_post_post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=True)

    post: Mapped[Optional["DBPost"]] = relationship(
        back_populates="likes",
    )


class DBCommentLike(Base):
    __tablename__ = "comment_like"

    id: Mapped[int] = mapped_column(sqltypes.Integer, primary_key=True, autoincrement=True)
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(sqltypes.DateTime, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(sqltypes.DateTime)
    updated_at: Mapped[datetime.datetime] = mapped_column(sqltypes.DateTime)

    _fk_user_user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)

    user: Mapped[Optional["DBUser"]] = relationship(
        back_populates="comment_likes",
    )

    _fk_comment_comment_id: Mapped[int] = mapped_column(ForeignKey("comment.id"), nullable=True)

    comment: Mapped[Optional["DBComment"]] = relationship(
        back_populates="likes",
    )


