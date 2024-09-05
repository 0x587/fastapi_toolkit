from typing import Optional

from fastapi_toolkit.define import Schema


class User(Schema):
    pass


class Item(Schema):
    value: int


class Range(Schema):
    min_value: int
    max_value: Optional[int]
