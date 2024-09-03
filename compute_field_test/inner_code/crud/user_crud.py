# generate_hash: c5afa47fd7a58d5c8a057690af226db0
"""
This file was automatically generated in 2024-09-03 17:14:42.825249
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
async def get_one(user_ident: int, db=Depends(get_db)) -> SchemaBaseUser:
    res = await db.get(DBUser, user_ident)
    if res and res.deleted_at is None:
        return res
    raise NOT_FOUND


async def batch_get(user_idents: List[int], db=Depends(get_db)) -> Page[SchemaBaseUser]:
    query = select(DBUser).filter(DBUser.deleted_at.is_(None)).filter(DBUser.id.in_(user_idents))
    return await paginate(db, query)


def get_all_query(
        filter_user_key: Optional[str] = None,
        sort_by: Optional[str] = None, is_desc: bool = False,
) -> Select:
    query = select(DBUser).filter(DBUser.deleted_at.is_(None))
    if filter_user_key is not None:
        query = query.filter(DBUser.user_key.__eq__(filter_user_key))
    if sort_by is not None:
        if is_desc:
            query = query.order_by(getattr(DBUser, sort_by).desc())
        else:
            query = query.order_by(getattr(DBUser, sort_by))
    return query


async def get_all(
        paginate_parmas: Params,
        query=Depends(get_all_query),
        db=Depends(get_db),
) -> Page[SchemaBaseUser]:
    return await paginate(db, query, params=paginate_parmas)


async def get_link_all(
        paginate_parmas: Params,
        query=Depends(get_all_query),
        db=Depends(get_db)
) -> Page[SchemaUser]:
    return await paginate(db, query, params=paginate_parmas)
# ---------------------User Query Routes----------------------


# -----------------------Create Routes------------------------
async def create_one(
        user_key: str,
        db=Depends(get_db)
) -> SchemaBaseUser:
    user = SchemaBaseUser(
        user_key=user_key,
    )
    user = DBUser(**user.model_dump())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return SchemaBaseUser.model_validate(user)


# -----------------------Update Routes------------------------
async def update_one(
        user_ident: int,
        user_key: Optional[str] = None,
        db=Depends(get_db)) -> SchemaBaseUser:
    res = await db.get(DBUser, user_ident)
    if not res or res.deleted_at is not None:
        raise NOT_FOUND
    if user_key is not None:
        res.user_key = user_key
    res.updated_at = datetime.datetime.now()
    await db.commit()
    await db.refresh(res)
    return SchemaBaseUser.model_validate(res)


# -----------------------Delete Routes------------------------
async def delete_one(user_ident: int, db=Depends(get_db)):
    res = await db.get(DBUser, user_ident)
    if not res or res.deleted_at is not None:
        raise NOT_FOUND
# TODO
    res.deleted_at = datetime.datetime.now()
    await db.commit()
    return {'message': 'Deleted', 'id': user_ident}


# ----------------------Relation Routes-----------------------

