import typing
from typing import Any
from pydantic_core import PydanticUndefined

from pydantic import BaseModel, Field as PydanticField


class Schema(BaseModel):
    class Config:
        from_attributes = True


def Field(
        default: Any = PydanticUndefined,
        default_factory: typing.Callable[[], Any] | None = None,
        alias: str | None = None,
        index: bool = False,
):
    return PydanticField(
        default=default,
        default_factory=default_factory,
        alias=alias,
        json_schema_extra={
            'index': index
        }
    )
