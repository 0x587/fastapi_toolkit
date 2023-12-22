import datetime
import uuid
from types import NoneType
from typing import Type

import pydantic
from sqlalchemy.sql import sqltypes


def build_in_mapping(t):
    type_map = {
        int: sqltypes.Integer,
        float: sqltypes.Float,
        str: sqltypes.String,
        bool: sqltypes.Boolean,
        bytes: sqltypes.LargeBinary,
        bytearray: sqltypes.LargeBinary,
    }
    return type_map.get(t, None)


def mapping(t):
    type_map = {
        uuid.UUID: sqltypes.UUID,
        pydantic.UUID1: sqltypes.UUID,
        pydantic.UUID3: sqltypes.UUID,
        pydantic.UUID4: sqltypes.UUID,
        pydantic.UUID5: sqltypes.UUID,
        datetime.datetime: sqltypes.DateTime,
        datetime.date: sqltypes.Date,
        datetime.timedelta: sqltypes.Interval,
    }
    return build_in_mapping(t) or type_map.get(t, NoneType)
