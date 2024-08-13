# generate_hash: 6d7024eb641a2f1c12ce078ad90496a5
"""
This file was automatically generated in 2024-08-14 00:21:38.634389
"""
import datetime
from typing import List, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.sql import sqltypes

from .db import Base


class DBUser(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(sqltypes.Integer, primary_key=True, autoincrement=True)
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(sqltypes.DateTime, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(sqltypes.DateTime)
    updated_at: Mapped[datetime.datetime] = mapped_column(sqltypes.DateTime)

    name: Mapped[str] = mapped_column(sqltypes.Text, nullable=False)

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


