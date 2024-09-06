# generate_hash: 554831fbd603249c69a270ae29d1417d
"""
This file was automatically generated in 2024-09-06 16:25:32.779121
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
def get_one(item_ident: int, db=Depends(get_db)) -> SchemaBaseItem:
    res = db.get(DBItem, item_ident)
    if res and res.deleted_at is None:
        return res
    raise NOT_FOUND


def batch_get(item_idents: List[int], db=Depends(get_db)) -> Page[SchemaBaseItem]:
    query = select(DBItem).filter(DBItem.deleted_at.is_(None)).filter(DBItem.id.in_(item_idents))
    return paginate(db, query)

class QueryParams(BaseModel):
    class SortParams(BaseModel):
        class StorFieldEnum(str, Enum):
            value = "value"

        field: StorFieldEnum
        is_desc: bool = False

    value: Optional[int] = None
    sort_by: List[SortParams] = Field(default_factory=list)

def get_all_query(params: QueryParams = Body()) -> Select:
    query = select(DBItem).filter(DBItem.deleted_at.is_(None))
    if params.value is not None:
        query = query.filter(DBItem.value.__eq__(params.value))
    for sort_item in params.sort_by:
        if sort_item.is_desc:
            query = query.order_by(getattr(DBItem, sort_item.field).desc())
        else:
            query = query.order_by(getattr(DBItem, sort_item.field))
    return query


def get_all(
        query=Depends(get_all_query),
        db=Depends(get_db),
) -> Page[SchemaBaseItem]:
    return paginate(db, query)


def get_link_all(
        query=Depends(get_all_query),
        db=Depends(get_db)
) -> Page[SchemaItem]:
    return paginate(db, query)
# ---------------------User Query Routes----------------------


# -----------------------Create Routes------------------------
def create_one(
        value: int,
        db=Depends(get_db)
) -> SchemaBaseItem:
    item = SchemaBaseItem(
        value=value,
    )
    item = DBItem(**item.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return SchemaBaseItem.model_validate(item)


# -----------------------Update Routes------------------------
def update_one(
        item_ident: int,
        value: Optional[int] = None,
        db=Depends(get_db)) -> SchemaBaseItem:
    res = db.get(DBItem, item_ident)
    if not res or res.deleted_at is not None:
        raise NOT_FOUND
    if value is not None:
        res.value = value
    res.updated_at = datetime.datetime.now()
    db.commit()
    db.refresh(res)
    return SchemaBaseItem.model_validate(res)


# -----------------------Delete Routes------------------------
def delete_one(item_ident: int, db=Depends(get_db)):
    res = db.get(DBItem, item_ident)
    if not res or res.deleted_at is not None:
        raise NOT_FOUND
# TODO
    res.deleted_at = datetime.datetime.now()
    db.commit()
    return {'message': 'Deleted', 'id': item_ident}


# ----------------------Relation Routes-----------------------

