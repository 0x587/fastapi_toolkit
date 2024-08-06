# generate_hash: e9d6c4fd6d61edf5b0618c3371e58335
"""
This file was automatically generated in 2024-08-06 22:49:59.086603
"""
import uuid
import datetime

from typing import List, Optional
from pydantic import computed_field, Field
from fastapi_toolkit.define import Schema

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import sqltypes

from ..db import Base


class DBUser(Base):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(sqltypes.Uuid, primary_key=True)
    username: Mapped[str] = mapped_column(sqltypes.String(256))
    hashed_password: Mapped[str] = mapped_column(sqltypes.String(1024))
    scopes: Mapped[Optional[str]] = mapped_column(sqltypes.String(1024), nullable=True)
    is_superuser: Mapped[bool] = mapped_column(sqltypes.Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(sqltypes.Boolean, default=False)

    registered_at: Mapped[datetime.datetime] = mapped_column(sqltypes.DateTime)
    activated_at: Mapped[Optional[datetime.datetime]] = mapped_column(sqltypes.DateTime, nullable=True)
    last_login_at: Mapped[Optional[datetime.datetime]] = mapped_column(sqltypes.DateTime, nullable=True)
    accessed_at: Mapped[Optional[datetime.datetime]] = mapped_column(sqltypes.DateTime, nullable=True)

    sex: Mapped[bool] = mapped_column(sqltypes.Boolean, nullable=False)


class Token(Schema):
    access_token: str
    token_type: str


class SchemaUser(Schema):
    id: uuid.UUID
    username: str
    scopes_: Optional[str] = Field(exclude=True, alias='scopes')

    @computed_field
    @property
    def scopes(self) -> List[str]:
        if self.scopes_:
            return self.scopes_.split()
        else:
            return []

    sex: bool = Field(nullable=False)


class SchemaUserFull(SchemaUser):
    is_superuser: bool
    is_active: bool
    registered_at: datetime.datetime
    activated_at: Optional[datetime.datetime]
    last_login_at: Optional[datetime.datetime]
    accessed_at: Optional[datetime.datetime]


class SchemaUserCreate(Schema):
    username: str
    password: str
    sex: bool = Field(nullable=False)

