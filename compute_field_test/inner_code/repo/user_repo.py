# generate_hash: e47e2ee11e06e0b26ccbeecd8e0d43d7
"""
This file was automatically generated in 2024-09-06 16:25:32.775552
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
def get_one(user_ident: int, db=Depends(get_db)) -> SchemaBaseUser:
    res = db.get(DBUser, user_ident)
    if res and res.deleted_at is None:
        return res
    raise NOT_FOUND


def batch_get(user_idents: List[int], db=Depends(get_db)) -> Page[SchemaBaseUser]:
    query = select(DBUser).filter(DBUser.deleted_at.is_(None)).filter(DBUser.id.in_(user_idents))
    return paginate(db, query)

class QueryParams(BaseModel):
    class SortParams(BaseModel):
        class StorFieldEnum(str, Enum):
            user_key = "user_key"

        field: StorFieldEnum
        is_desc: bool = False

    user_key: Optional[str] = None
    user_key_like: Optional[str] = None
    sort_by: List[SortParams] = Field(default_factory=list)

def get_all_query(params: QueryParams = Body()) -> Select:
    query = select(DBUser).filter(DBUser.deleted_at.is_(None))
    if params.user_key is not None:
        query = query.filter(DBUser.user_key.__eq__(params.user_key))
    if params.user_key_like is not None:
        query = query.filter(DBUser.user_key.like(params.user_key_like))
    for sort_item in params.sort_by:
        if sort_item.is_desc:
            query = query.order_by(getattr(DBUser, sort_item.field).desc())
        else:
            query = query.order_by(getattr(DBUser, sort_item.field))
    return query


def get_all(
        query=Depends(get_all_query),
        db=Depends(get_db),
) -> Page[SchemaBaseUser]:
    return paginate(db, query)


def get_link_all(
        query=Depends(get_all_query),
        db=Depends(get_db)
) -> Page[SchemaUser]:
    return paginate(db, query)
# ---------------------User Query Routes----------------------


# -----------------------Create Routes------------------------
def create_one(
        user_key: str,
        db=Depends(get_db)
) -> SchemaBaseUser:
    user = SchemaBaseUser(
        user_key=user_key,
    )
    user = DBUser(**user.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return SchemaBaseUser.model_validate(user)


# -----------------------Update Routes------------------------
def update_one(
        user_ident: int,
        user_key: Optional[str] = None,
        db=Depends(get_db)) -> SchemaBaseUser:
    res = db.get(DBUser, user_ident)
    if not res or res.deleted_at is not None:
        raise NOT_FOUND
    if user_key is not None:
        res.user_key = user_key
    res.updated_at = datetime.datetime.now()
    db.commit()
    db.refresh(res)
    return SchemaBaseUser.model_validate(res)


# -----------------------Delete Routes------------------------
def delete_one(user_ident: int, db=Depends(get_db)):
    res = db.get(DBUser, user_ident)
    if not res or res.deleted_at is not None:
        raise NOT_FOUND
# TODO
    res.deleted_at = datetime.datetime.now()
    db.commit()
    return {'message': 'Deleted', 'id': user_ident}


# ----------------------Relation Routes-----------------------

