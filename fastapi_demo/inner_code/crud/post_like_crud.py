# generate_hash: e218b27095dbeb0a129b6f9e3067a37b
"""
This file was automatically generated in 2024-08-14 00:21:54.794753
"""

from typing import List, Optional
from fastapi import Depends, Response, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
import datetime
from sqlalchemy import select, Select
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


async def __get_all_query(
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
        query=Depends(__get_all_query),
        db=Depends(get_db)
) -> Page[SchemaBasePostLike]:
    return await paginate(db, query)


async def get_link_all(
        query=Depends(__get_all_query),
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


async def get_all_is_user_id_query(user_id: int):
    query = await __get_all_query()
    return query.join(DBUser).filter(DBUser.id.__eq__(user_id))                    
                    

async def get_all_is_user_id(user_id: int, db=Depends(get_db)) -> List[SchemaPostLike]:
    query = await __get_all_query()
    query = query.join(DBUser).filter(DBUser.id.__eq__(user_id))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_is_user_query(user: SchemaBaseUser):
    query = await __get_all_query()
    return query.join(DBUser).filter(DBUser.id.__eq__(user.id))                    
                    

async def get_all_is_user(user: SchemaBaseUser, db=Depends(get_db)) -> List[SchemaPostLike]:
    query = await __get_all_query()
    query = query.join(DBUser).filter(DBUser.id.__eq__(user.id))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_has_user_id_query(user_ids: List[int]):
    query = await __get_all_query()
    return query.join(DBUser).filter(DBUser.id.in_(user_ids))                    
                    

async def get_all_has_user_id(user_ids: List[int], db=Depends(get_db)) -> List[SchemaPostLike]:
    query = await __get_all_query()
    query = query.join(DBUser).filter(DBUser.id.in_(user_ids))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_has_user_query(users: List[SchemaBaseUser]):
    query = await __get_all_query()
    return query.join(DBUser).filter(DBUser.id.in_(map(lambda x: x.id, users)))                    
                    

async def get_all_has_user(users: List[SchemaBaseUser], db=Depends(get_db)) -> List[SchemaPostLike]:
    query = await __get_all_query()
    query = query.join(DBUser).filter(DBUser.id.in_(map(lambda x: x.id, users)))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_is_post_id_query(post_id: int):
    query = await __get_all_query()
    return query.join(DBPost).filter(DBPost.id.__eq__(post_id))                    
                    

async def get_all_is_post_id(post_id: int, db=Depends(get_db)) -> List[SchemaPostLike]:
    query = await __get_all_query()
    query = query.join(DBPost).filter(DBPost.id.__eq__(post_id))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_is_post_query(post: SchemaBasePost):
    query = await __get_all_query()
    return query.join(DBPost).filter(DBPost.id.__eq__(post.id))                    
                    

async def get_all_is_post(post: SchemaBasePost, db=Depends(get_db)) -> List[SchemaPostLike]:
    query = await __get_all_query()
    query = query.join(DBPost).filter(DBPost.id.__eq__(post.id))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_has_post_id_query(post_ids: List[int]):
    query = await __get_all_query()
    return query.join(DBPost).filter(DBPost.id.in_(post_ids))                    
                    

async def get_all_has_post_id(post_ids: List[int], db=Depends(get_db)) -> List[SchemaPostLike]:
    query = await __get_all_query()
    query = query.join(DBPost).filter(DBPost.id.in_(post_ids))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_has_post_query(posts: List[SchemaBasePost]):
    query = await __get_all_query()
    return query.join(DBPost).filter(DBPost.id.in_(map(lambda x: x.id, posts)))                    
                    

async def get_all_has_post(posts: List[SchemaBasePost], db=Depends(get_db)) -> List[SchemaPostLike]:
    query = await __get_all_query()
    query = query.join(DBPost).filter(DBPost.id.in_(map(lambda x: x.id, posts)))     
    return (await db.scalars(query)).all()                  
                    
