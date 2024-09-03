# generate_hash: e2492a232838a8f1aaae7fca4185f1d5
"""
This file was automatically generated in 2024-09-03 17:14:42.828781
"""

from typing import List, Optional
from fastapi import Depends, Response, HTTPException, status
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
import datetime
from sqlalchemy import select, Select
from sqlalchemy.orm import joinedload, selectinload
from ..db import get_db
from ..models import *
from ..schemas import *

NOT_FOUND = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item Not found")


# ------------------------Query Routes------------------------
async def get_one(item_ident: int, db=Depends(get_db)) -> SchemaBaseItem:
    res = await db.get(DBItem, item_ident)
    if res and res.deleted_at is None:
        return res
    raise NOT_FOUND


async def batch_get(item_idents: List[int], db=Depends(get_db)) -> Page[SchemaBaseItem]:
    query = select(DBItem).filter(DBItem.deleted_at.is_(None)).filter(DBItem.id.in_(item_idents))
    return await paginate(db, query)


def get_all_query(
        filter_value: Optional[int] = None,
        sort_by: Optional[str] = None, is_desc: bool = False,
) -> Select:
    query = select(DBItem).filter(DBItem.deleted_at.is_(None))
    if filter_value is not None:
        query = query.filter(DBItem.value.__eq__(filter_value))
    if sort_by is not None:
        if is_desc:
            query = query.order_by(getattr(DBItem, sort_by).desc())
        else:
            query = query.order_by(getattr(DBItem, sort_by))
    return query


async def get_all(
        paginate_parmas: Params,
        query=Depends(get_all_query),
        db=Depends(get_db),
) -> Page[SchemaBaseItem]:
    return await paginate(db, query, params=paginate_parmas)


async def get_link_all(
        paginate_parmas: Params,
        query=Depends(get_all_query),
        db=Depends(get_db)
) -> Page[SchemaItem]:
    return await paginate(db, query, params=paginate_parmas)
# ---------------------User Query Routes----------------------


# -----------------------Create Routes------------------------
async def create_one(
        value: int,
        db=Depends(get_db)
) -> SchemaBaseItem:
    item = SchemaBaseItem(
        value=value,
    )
    item = DBItem(**item.model_dump())
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return SchemaBaseItem.model_validate(item)


# -----------------------Update Routes------------------------
async def update_one(
        item_ident: int,
        value: Optional[int] = None,
        db=Depends(get_db)) -> SchemaBaseItem:
    res = await db.get(DBItem, item_ident)
    if not res or res.deleted_at is not None:
        raise NOT_FOUND
    if value is not None:
        res.value = value
    res.updated_at = datetime.datetime.now()
    await db.commit()
    await db.refresh(res)
    return SchemaBaseItem.model_validate(res)


# -----------------------Delete Routes------------------------
async def delete_one(item_ident: int, db=Depends(get_db)):
    res = await db.get(DBItem, item_ident)
    if not res or res.deleted_at is not None:
        raise NOT_FOUND
# TODO
    res.deleted_at = datetime.datetime.now()
    await db.commit()
    return {'message': 'Deleted', 'id': item_ident}


# ----------------------Relation Routes-----------------------

