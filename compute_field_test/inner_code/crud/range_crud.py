# generate_hash: d14c3e9c7048f788f46f86f557026eaf
"""
This file was automatically generated in 2024-09-01 22:59:02.276620
"""

from typing import List, Optional
from fastapi import Depends, Response, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
import datetime
from sqlalchemy import select, Select
from sqlalchemy.orm import joinedload, selectinload
from ..db import get_db
from ..models import *
from ..schemas import *

NOT_FOUND = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item Not found")


# ------------------------Query Routes------------------------
async def get_one(ident: int, db=Depends(get_db)) -> SchemaBaseRange:
    res = await db.get(DBRange, ident)
    if res and res.deleted_at is None:
        return res
    raise NOT_FOUND


async def batch_get(idents: List[int], db=Depends(get_db)) -> Page[SchemaBaseRange]:
    query = select(DBRange).filter(DBRange.deleted_at.is_(None)).filter(DBRange.id.in_(idents))
    return await paginate(db, query)


def get_all_query(
        filter_min_value: Optional[int] = None,
        filter_max_value: Optional[int] = None,
        sort_by: Optional[str] = None, is_desc: bool = False,
) -> Select:
    query = select(DBRange).filter(DBRange.deleted_at.is_(None))
    if filter_min_value is not None:
        query = query.filter(DBRange.min_value.__eq__(filter_min_value))
    if filter_max_value is not None:
        query = query.filter(DBRange.max_value.__eq__(filter_max_value))
    if sort_by is not None:
        if is_desc:
            query = query.order_by(getattr(DBRange, sort_by).desc())
        else:
            query = query.order_by(getattr(DBRange, sort_by))
    return query


async def get_all(
        query=Depends(get_all_query),
        db=Depends(get_db)
) -> Page[SchemaBaseRange]:
    return await paginate(db, query)


async def get_link_all(
        query=Depends(get_all_query),
        db=Depends(get_db)
) -> Page[SchemaRange]:
    return await paginate(db, query)
# ---------------------User Query Routes----------------------


# -----------------------Create Routes------------------------
async def create_one(
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
    await db.commit()
    await db.refresh(range)
    return SchemaBaseRange.model_validate(range)


# -----------------------Update Routes------------------------
async def update_one(
        ident: int,
        min_value: Optional[int] = None,
        max_value: Optional[int] = None,
        db=Depends(get_db)) -> SchemaBaseRange:
    res = await db.get(DBRange, ident)
    if not res or res.deleted_at is not None:
        raise NOT_FOUND
    if min_value is not None:
        res.min_value = min_value
    if max_value is not None:
        res.max_value = max_value
    res.updated_at = datetime.datetime.now()
    await db.commit()
    await db.refresh(res)
    return SchemaBaseRange.model_validate(res)


# -----------------------Delete Routes------------------------
async def delete_one(ident: int, db=Depends(get_db)):
    res = await db.get(DBRange, ident)
    if not res or res.deleted_at is not None:
        raise NOT_FOUND
# TODO
    res.deleted_at = datetime.datetime.now()
    await db.commit()
    return {'message': 'Deleted', 'id': ident}


# ----------------------Relation Routes-----------------------

