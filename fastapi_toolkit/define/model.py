from pydantic import BaseModel
from sqlmodel import SQLModel, Field


class Schema(SQLModel):
    id: int = Field(primary_key=True)


def mark(cls):
    print(cls)
    return cls
