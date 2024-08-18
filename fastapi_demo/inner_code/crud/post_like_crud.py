# generate_hash: a990195a3503dc8ff534c99327fa1f14
"""
This file was automatically generated in 2024-08-18 15:51:57.932077
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
async def get_one(ident: int, db=Depends(get_db)) -> SchemaBasePostLike:
    res = await db.get(DBPostLike, ident)
    if res and res.deleted_at is None:
        return res
    raise NOT_FOUND


async def batch_get(idents: List[int], db=Depends(get_db)) -> Page[SchemaBasePostLike]:
    query = select(DBPostLike).filter(DBPostLike.deleted_at.is_(None)).filter(DBPostLike.id.in_(idents))
    return await paginate(db, query)


def get_all_query(
        sort_by: Optional[str] = None, is_desc: bool = False,
) -> Select:
    query = select(DBPostLike).filter(DBPostLike.deleted_at.is_(None))
    if sort_by is not None:
        if is_desc:
            query = query.order_by(getattr(DBPostLike, sort_by).desc())
        else:
            query = query.order_by(getattr(DBPostLike, sort_by))
    return query


async def get_all(
        query=Depends(get_all_query),
        db=Depends(get_db)
) -> Page[SchemaBasePostLike]:
    return await paginate(db, query)


async def get_link_all(
        query=Depends(get_all_query),
        db=Depends(get_db)
) -> Page[SchemaPostLike]:
    return await paginate(db, query)
# ---------------------User Query Routes----------------------


# -----------------------Create Routes------------------------
async def create_one(
        db=Depends(get_db)
) -> SchemaBasePostLike:
    post_like = SchemaBasePostLike(
    )
    post_like = DBPostLike(**post_like.model_dump())
    db.add(post_like)
    await db.commit()
    await db.refresh(post_like)
    return SchemaBasePostLike.model_validate(post_like)


# -----------------------Update Routes------------------------
async def update_one(
        ident: int,
        db=Depends(get_db)) -> SchemaBasePostLike:
    res = await db.get(DBPostLike, ident)
    if not res or res.deleted_at is not None:
        raise NOT_FOUND
    res.updated_at = datetime.datetime.now()
    await db.commit()
    await db.refresh(res)
    return SchemaBasePostLike.model_validate(res)


# -----------------------Delete Routes------------------------
async def delete_one(ident: int, db=Depends(get_db)):
    res = await db.get(DBPostLike, ident)
    if not res or res.deleted_at is not None:
        raise NOT_FOUND
# TODO
    res.deleted_at = datetime.datetime.now()
    await db.commit()
    return {'message': 'Deleted', 'id': ident}


# ----------------------Relation Routes-----------------------


def get_user_id_is_query(user_id: int) -> Select:
    query = get_all_query()
    query = query.join(DBUser).filter(DBUser.id.__eq__(user_id))
    query = query.options(joinedload(DBPostLike.user))
    query = query.options(joinedload(DBPostLike.post))
    return query
                

async def get_user_id_is(user_id: int, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaPostLike]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBUser).filter(DBUser.id.__eq__(user_id))
    query = query.options(joinedload(DBPostLike.user))
    query = query.options(joinedload(DBPostLike.post))
    return (await db.scalars(query)).all()
                

def get_user_is_query(user: SchemaBaseUser) -> Select:
    query = get_all_query()
    query = query.join(DBUser).filter(DBUser.id.__eq__(user.id))
    query = query.options(joinedload(DBPostLike.user))
    query = query.options(joinedload(DBPostLike.post))
    return query
                

async def get_user_is(user: SchemaBaseUser, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaPostLike]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBUser).filter(DBUser.id.__eq__(user.id))
    query = query.options(joinedload(DBPostLike.user))
    query = query.options(joinedload(DBPostLike.post))
    return (await db.scalars(query)).all()
                

def get_user_id_has_query(user_ids: List[int]) -> Select:
    query = get_all_query()
    query = query.join(DBUser).filter(DBUser.id.in_(user_ids))
    query = query.options(joinedload(DBPostLike.user))
    query = query.options(joinedload(DBPostLike.post))
    return query
                

async def get_user_id_has(user_ids: List[int], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaPostLike]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBUser).filter(DBUser.id.in_(user_ids))
    query = query.options(joinedload(DBPostLike.user))
    query = query.options(joinedload(DBPostLike.post))
    return (await db.scalars(query)).all()
                

def get_user_has_query(users: List[SchemaBaseUser]) -> Select:
    query = get_all_query()
    query = query.join(DBUser).filter(DBUser.id.in_(map(lambda x: x.id, users)))
    query = query.options(joinedload(DBPostLike.user))
    query = query.options(joinedload(DBPostLike.post))
    return query
                

async def get_user_has(users: List[SchemaBaseUser], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaPostLike]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBUser).filter(DBUser.id.in_(map(lambda x: x.id, users)))
    query = query.options(joinedload(DBPostLike.user))
    query = query.options(joinedload(DBPostLike.post))
    return (await db.scalars(query)).all()
                

def get_post_id_is_query(post_id: int) -> Select:
    query = get_all_query()
    query = query.join(DBPost).filter(DBPost.id.__eq__(post_id))
    query = query.options(joinedload(DBPostLike.user))
    query = query.options(joinedload(DBPostLike.post))
    return query
                

async def get_post_id_is(post_id: int, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaPostLike]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBPost).filter(DBPost.id.__eq__(post_id))
    query = query.options(joinedload(DBPostLike.user))
    query = query.options(joinedload(DBPostLike.post))
    return (await db.scalars(query)).all()
                

def get_post_is_query(post: SchemaBasePost) -> Select:
    query = get_all_query()
    query = query.join(DBPost).filter(DBPost.id.__eq__(post.id))
    query = query.options(joinedload(DBPostLike.user))
    query = query.options(joinedload(DBPostLike.post))
    return query
                

async def get_post_is(post: SchemaBasePost, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaPostLike]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBPost).filter(DBPost.id.__eq__(post.id))
    query = query.options(joinedload(DBPostLike.user))
    query = query.options(joinedload(DBPostLike.post))
    return (await db.scalars(query)).all()
                

def get_post_id_has_query(post_ids: List[int]) -> Select:
    query = get_all_query()
    query = query.join(DBPost).filter(DBPost.id.in_(post_ids))
    query = query.options(joinedload(DBPostLike.user))
    query = query.options(joinedload(DBPostLike.post))
    return query
                

async def get_post_id_has(post_ids: List[int], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaPostLike]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBPost).filter(DBPost.id.in_(post_ids))
    query = query.options(joinedload(DBPostLike.user))
    query = query.options(joinedload(DBPostLike.post))
    return (await db.scalars(query)).all()
                

def get_post_has_query(posts: List[SchemaBasePost]) -> Select:
    query = get_all_query()
    query = query.join(DBPost).filter(DBPost.id.in_(map(lambda x: x.id, posts)))
    query = query.options(joinedload(DBPostLike.user))
    query = query.options(joinedload(DBPostLike.post))
    return query
                

async def get_post_has(posts: List[SchemaBasePost], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaPostLike]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBPost).filter(DBPost.id.in_(map(lambda x: x.id, posts)))
    query = query.options(joinedload(DBPostLike.user))
    query = query.options(joinedload(DBPostLike.post))
    return (await db.scalars(query)).all()
                
