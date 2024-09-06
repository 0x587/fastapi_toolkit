# generate_hash: a9d5c0835257aee7021eec7e47a2fe0c
"""
This file was automatically generated in 2024-09-06 16:25:32.780292
"""
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from fastapi import Depends, Body, Response, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
import datetime
from sqlalchemy import select, Select
from sqlalchemy.orm import joinedload, selectinload
from ..db import get_db_sync as get_db
from ..models import *
from ..schemas import *

NOT_FOUND = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item Not found")


# ------------------------Query Routes------------------------
def get_one(range_ident: int, db=Depends(get_db)) -> SchemaBaseRange:
    res = db.get(DBRange, range_ident)
    if res and res.deleted_at is None:
        return res
    raise NOT_FOUND


def batch_get(range_idents: List[int], db=Depends(get_db)) -> Page[SchemaBaseRange]:
    query = select(DBRange).filter(DBRange.deleted_at.is_(None)).filter(DBRange.id.in_(range_idents))
    return paginate(db, query)

class QueryParams(BaseModel):
    class SortParams(BaseModel):
        class StorFieldEnum(str, Enum):
            min_value = "min_value"
            max_value = "max_value"

        field: StorFieldEnum
        is_desc: bool = False

    min_value: Optional[int] = None
    max_value: Optional[int] = None
    sort_by: List[SortParams] = Field(default_factory=list)

def get_all_query(params: QueryParams = Body()) -> Select:
    query = select(DBRange).filter(DBRange.deleted_at.is_(None))
    if params.min_value is not None:
        query = query.filter(DBRange.min_value.__eq__(params.min_value))
    if params.max_value is not None:
        query = query.filter(DBRange.max_value.__eq__(params.max_value))
    for sort_item in params.sort_by:
        if sort_item.is_desc:
            query = query.order_by(getattr(DBRange, sort_item.field).desc())
        else:
            query = query.order_by(getattr(DBRange, sort_item.field))
    return query


def get_all(
        query=Depends(get_all_query),
        db=Depends(get_db),
) -> Page[SchemaBaseRange]:
    return paginate(db, query)


def get_link_all(
        query=Depends(get_all_query),
        db=Depends(get_db)
) -> Page[SchemaRange]:
    return paginate(db, query)
# ---------------------User Query Routes----------------------


# -----------------------Create Routes------------------------
def create_one(
        min_value: int,
        max_value: int,
        db=Depends(get_db)
) -> SchemaBaseRange:
    range = SchemaBaseRange(
        min_value=min_value,
        max_value=max_value,
    )
    range = DBRange(**range.model_dump())
    db.add(range)
    db.commit()
    db.refresh(range)
    return SchemaBaseRange.model_validate(range)


# -----------------------Update Routes------------------------
def update_one(
        range_ident: int,
        min_value: Optional[int] = None,
        max_value: Optional[int] = None,
        db=Depends(get_db)) -> SchemaBaseRange:
    res = db.get(DBRange, range_ident)
    if not res or res.deleted_at is not None:
        raise NOT_FOUND
    if min_value is not None:
        res.min_value = min_value
    if max_value is not None:
        res.max_value = max_value
    res.updated_at = datetime.datetime.now()
    db.commit()
    db.refresh(res)
    return SchemaBaseRange.model_validate(res)


# -----------------------Delete Routes------------------------
def delete_one(range_ident: int, db=Depends(get_db)):
    res = db.get(DBRange, range_ident)
    if not res or res.deleted_at is not None:
        raise NOT_FOUND
# TODO
    res.deleted_at = datetime.datetime.now()
    db.commit()
    return {'message': 'Deleted', 'id': range_ident}


# ----------------------Relation Routes-----------------------

