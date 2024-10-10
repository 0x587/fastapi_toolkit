# generate_hash: a95ffe5e6f82b0fbefad11a583a0ca37
"""
This file was automatically generated in 2024-10-10 15:31:22.024373
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

    sex: Mapped[bool] = mapped_column(sqltypes.Boolean, nullable=False, index=False)
    title: Mapped[str] = mapped_column(sqltypes.Text, nullable=False, index=False)
    name: Mapped[str] = mapped_column(sqltypes.Text, nullable=False, index=True)
    desc: Mapped[str] = mapped_column(sqltypes.Text, nullable=False, index=False)
    bg_img: Mapped[str] = mapped_column(sqltypes.Text, nullable=False, index=False)
    hot_level: Mapped[int] = mapped_column(sqltypes.Integer, nullable=False, index=False)
    star_level: Mapped[int] = mapped_column(sqltypes.Integer, nullable=False, index=False)
    user_key: Mapped[str] = mapped_column(sqltypes.Text, nullable=False, index=True)
    avatar: Mapped[Optional[str]] = mapped_column(sqltypes.Text, nullable=True, index=False)

    info_blocks: Mapped[List["DBInfoBlock"]] = relationship(
        back_populates="user",
    )

    certified_records: Mapped[List["DBCertifiedRecord"]] = relationship(
        back_populates="user",
    )


class DBInfoBlock(Base):
    __tablename__ = "info_block"

    id: Mapped[int] = mapped_column(sqltypes.Integer, primary_key=True, autoincrement=True)
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(sqltypes.DateTime, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(sqltypes.DateTime)
    updated_at: Mapped[datetime.datetime] = mapped_column(sqltypes.DateTime)

    type: Mapped[str] = mapped_column(sqltypes.Text, nullable=False, index=False)
    title: Mapped[str] = mapped_column(sqltypes.Text, nullable=False, index=False)
    sub_title: Mapped[str] = mapped_column(sqltypes.Text, nullable=False, index=False)
    desc: Mapped[str] = mapped_column(sqltypes.Text, nullable=False, index=False)
    tags: Mapped[str] = mapped_column(sqltypes.Text, nullable=False, index=False)
    time_start: Mapped[datetime.date] = mapped_column(sqltypes.Date, nullable=False, index=False)
    time_end: Mapped[datetime.date] = mapped_column(sqltypes.Date, nullable=False, index=False)
    show: Mapped[bool] = mapped_column(sqltypes.Boolean, nullable=False, index=False)

    _fk_user_user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    user: Mapped[Optional["DBUser"]] = relationship(
        back_populates="info_blocks",
    )

    certified_records: Mapped[List["DBCertifiedRecord"]] = relationship(
        back_populates="info_block",
    )


class DBCertifiedRecord(Base):
    __tablename__ = "certified_record"

    id: Mapped[int] = mapped_column(sqltypes.Integer, primary_key=True, autoincrement=True)
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(sqltypes.DateTime, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(sqltypes.DateTime)
    updated_at: Mapped[datetime.datetime] = mapped_column(sqltypes.DateTime)

    done: Mapped[bool] = mapped_column(sqltypes.Boolean, nullable=False, index=False)
    target_real_name: Mapped[str] = mapped_column(sqltypes.Text, nullable=False, index=False)
    self_real_name: Mapped[str] = mapped_column(sqltypes.Text, nullable=False, index=False)
    relation: Mapped[str] = mapped_column(sqltypes.Text, nullable=False, index=False)

    _fk_user_user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    user: Mapped[Optional["DBUser"]] = relationship(
        back_populates="certified_records",
    )

    _fk_info_block_info_block_id: Mapped[int] = mapped_column(ForeignKey("info_block.id"), nullable=True)
    info_block: Mapped[Optional["DBInfoBlock"]] = relationship(
        back_populates="certified_records",
    )


__all__ = [
    'Base',
    'DBUser',
    'DBInfoBlock',
    'DBCertifiedRecord',
]