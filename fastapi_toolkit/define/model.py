import datetime
from typing import Optional

from pydantic import BaseModel
from sqlmodel import SQLModel, Field


class Schema(SQLModel):
    id: int = Field(primary_key=True)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now, exclude=True)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now, exclude=True)
    deleted_at: Optional[datetime.datetime] = Field(default=None, index=True, exclude=True)


def mark(cls):
    print(cls)
    return cls
