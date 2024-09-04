# generate_hash: 486345461547b20795633bd8886437bc
"""
This file was automatically generated in 2024-09-04 15:56:04.567719
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

    user_key: Mapped[str] = mapped_column(sqltypes.Text, nullable=False)


class DBItem(Base):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(sqltypes.Integer, primary_key=True, autoincrement=True)
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(sqltypes.DateTime, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(sqltypes.DateTime)
    updated_at: Mapped[datetime.datetime] = mapped_column(sqltypes.DateTime)

    value: Mapped[int] = mapped_column(sqltypes.Integer, nullable=False)


class DBRange(Base):
    __tablename__ = "range"

    id: Mapped[int] = mapped_column(sqltypes.Integer, primary_key=True, autoincrement=True)
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(sqltypes.DateTime, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(sqltypes.DateTime)
    updated_at: Mapped[datetime.datetime] = mapped_column(sqltypes.DateTime)

    min_value: Mapped[int] = mapped_column(sqltypes.Integer, nullable=False)

    max_value: Mapped[int] = mapped_column(sqltypes.Integer, nullable=False)


__all__ = [
    'DBUser',
    'DBItem',
    'DBRange',
]