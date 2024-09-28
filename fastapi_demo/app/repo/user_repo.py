# generate_hash: 7d6047c46976e12fed295a4408a295d5
"""
This file was automatically generated in 2024-09-29 00:28:32.141821
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

NOT_FOUND = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item Not found")


# ------------------------Query Routes------------------------
def get_one(user_ident: int, db=Depends(get_db)) -> User:
    res = db.get(User, user_ident)
    if res and res.deleted_at is None:
        return res
    raise NOT_FOUND


def batch_get(user_idents: List[int], db=Depends(get_db)) -> Page[User]:
    query = select(User).filter(User.deleted_at.is_(None)).filter(User.id.in_(user_idents))
    return paginate(db, query)

class QueryParams(BaseModel):
    class SortParams(BaseModel):
        class StorFieldEnum(str, Enum):
            id = "id"
            title = "title"
            name = "name"
            desc = "desc"
            bg_img = "bg_img"
            hot_level = "hot_level"
            star_level = "star_level"
            sex = "sex"
            avatar = "avatar"

        field: StorFieldEnum
        is_desc: bool = False

    id: Optional[int] = None,
    title: Optional[str] = None,
    title_like: Optional[str] = None,
    name: Optional[str] = None,
    name_like: Optional[str] = None,
    desc: Optional[str] = None,
    desc_like: Optional[str] = None,
    bg_img: Optional[str] = None,
    bg_img_like: Optional[str] = None,
    hot_level: Optional[int] = None,
    star_level: Optional[int] = None,
    sex: Optional[bool] = None,
    avatar: Optional[str] = None,
    avatar_like: Optional[str] = None,
    sort_by: List[SortParams] = Field(default_factory=list)

def get_all_query(params: QueryParams = Body()) -> Select:
    query = select(User).filter(User.deleted_at.is_(None))
    if params.id is not None:
        query = query.filter(User.id.__eq__(params.id))
    if params.title is not None:
        query = query.filter(User.title.__eq__(params.title))
    if params.title_like is not None:
        query = query.filter(User.title.like(params.title_like))
    if params.name is not None:
        query = query.filter(User.name.__eq__(params.name))
    if params.name_like is not None:
        query = query.filter(User.name.like(params.name_like))
    if params.desc is not None:
        query = query.filter(User.desc.__eq__(params.desc))
    if params.desc_like is not None:
        query = query.filter(User.desc.like(params.desc_like))
    if params.bg_img is not None:
        query = query.filter(User.bg_img.__eq__(params.bg_img))
    if params.bg_img_like is not None:
        query = query.filter(User.bg_img.like(params.bg_img_like))
    if params.hot_level is not None:
        query = query.filter(User.hot_level.__eq__(params.hot_level))
    if params.star_level is not None:
        query = query.filter(User.star_level.__eq__(params.star_level))
    if params.sex is not None:
        query = query.filter(User.sex.__eq__(params.sex))
    if params.avatar is not None:
        query = query.filter(User.avatar.__eq__(params.avatar))
    for sort_item in params.sort_by:
        if sort_item.is_desc:
            query = query.order_by(getattr(User, sort_item.field).desc())
        else:
            query = query.order_by(getattr(User, sort_item.field))
    return query


def get_all(
        query=Depends(get_all_query),
        db=Depends(get_db),
) -> Page[User]:
    return paginate(db, query)

# ---------------------User Query Routes----------------------


# -----------------------Create Routes------------------------
def create_one_model(model: User, db=Depends(get_db)) -> User:
    user = User(**model.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_one(
        id: int,
        title: str,
        name: str,
        desc: str,
        bg_img: str,
        hot_level: int,
        star_level: int,
        sex: bool = True,
        avatar: Optional[str] = None,
        db=Depends(get_db)
) -> User:
    user = User(
        id=id,
        title=title,
        name=name,
        desc=desc,
        bg_img=bg_img,
        hot_level=hot_level,
        star_level=star_level,
        sex=sex,
        avatar=avatar,
    )
    return create_one_model(user, db)


# -----------------------Update Routes------------------------
def update_one(
        user_ident: int,
        id: Optional[int] = None,
        title: Optional[str] = None,
        name: Optional[str] = None,
        desc: Optional[str] = None,
        bg_img: Optional[str] = None,
        hot_level: Optional[int] = None,
        star_level: Optional[int] = None,
        sex: Optional[bool] = None,
        avatar: Optional[str] = None,
        db=Depends(get_db)) -> User:
    res = db.get(User, user_ident)
    if not res or res.deleted_at is not None:
        raise NOT_FOUND
    if id is not None:
        res.id = id
    if title is not None:
        res.title = title
    if name is not None:
        res.name = name
    if desc is not None:
        res.desc = desc
    if bg_img is not None:
        res.bg_img = bg_img
    if hot_level is not None:
        res.hot_level = hot_level
    if star_level is not None:
        res.star_level = star_level
    if sex is not None:
        res.sex = sex
    if avatar is not None:
        res.avatar = avatar
    res.updated_at = datetime.datetime.now()
    db.commit()
    db.refresh(res)
    return User.model_validate(res)


# -----------------------Delete Routes------------------------
def delete_one(user_ident: int, db=Depends(get_db)):
    res = db.get(User, user_ident)
    if not res or res.deleted_at is not None:
        raise NOT_FOUND
# TODO
    res.deleted_at = datetime.datetime.now()
    db.commit()
    return {'message': 'Deleted', 'id': user_ident}


# ----------------------Relation Routes-----------------------

