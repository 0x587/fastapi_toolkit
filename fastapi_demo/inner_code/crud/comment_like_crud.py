# generate_hash: 25be65436d5df7f28b1a7ce216bf09a2
"""
This file was automatically generated in 2024-08-14 00:21:54.795096
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
async def get_one(ident: int, db=Depends(get_db)) -> SchemaBaseCommentLike:
    res = await db.get(DBCommentLike, ident)
    if res and res.deleted_at is None:
        return res
    raise NOT_FOUND


async def batch_get(idents: List[int], db=Depends(get_db)) -> Page[SchemaBaseCommentLike]:
    query = select(DBCommentLike).filter(DBCommentLike.deleted_at.is_(None)).filter(DBCommentLike.id.in_(idents))
    return await paginate(db, query)


async def __get_all_query(
        sort_by: Optional[str] = None, is_desc: bool = False,
) -> Select:
    query = select(DBCommentLike).filter(DBCommentLike.deleted_at.is_(None))
    if sort_by is not None:
        if is_desc:
            query = query.order_by(getattr(DBCommentLike, sort_by).desc())
        else:
            query = query.order_by(getattr(DBCommentLike, sort_by))
    return query


async def get_all(
        query=Depends(__get_all_query),
        db=Depends(get_db)
) -> Page[SchemaBaseCommentLike]:
    return await paginate(db, query)


async def get_link_all(
        query=Depends(__get_all_query),
        db=Depends(get_db)
) -> Page[SchemaCommentLike]:
    return await paginate(db, query)
# ---------------------User Query Routes----------------------


# -----------------------Create Routes------------------------
async def create_one(
        db=Depends(get_db)
) -> SchemaBaseCommentLike:
    comment_like = SchemaBaseCommentLike(
    )
    comment_like = DBCommentLike(**comment_like.model_dump())
    db.add(comment_like)
    await db.commit()
    await db.refresh(comment_like)
    return SchemaBaseCommentLike.model_validate(comment_like)


# -----------------------Update Routes------------------------
async def update_one(
        ident: int,
        db=Depends(get_db)) -> SchemaBaseCommentLike:
    res = await db.get(DBCommentLike, ident)
    if not res or res.deleted_at is not None:
        raise NOT_FOUND
    res.updated_at = datetime.datetime.now()
    await db.commit()
    await db.refresh(res)
    return SchemaBaseCommentLike.model_validate(res)


# -----------------------Delete Routes------------------------
async def delete_one(ident: int, db=Depends(get_db)):
    res = await db.get(DBCommentLike, ident)
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
                    

async def get_all_is_user_id(user_id: int, db=Depends(get_db)) -> List[SchemaCommentLike]:
    query = await __get_all_query()
    query = query.join(DBUser).filter(DBUser.id.__eq__(user_id))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_is_user_query(user: SchemaBaseUser):
    query = await __get_all_query()
    return query.join(DBUser).filter(DBUser.id.__eq__(user.id))                    
                    

async def get_all_is_user(user: SchemaBaseUser, db=Depends(get_db)) -> List[SchemaCommentLike]:
    query = await __get_all_query()
    query = query.join(DBUser).filter(DBUser.id.__eq__(user.id))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_has_user_id_query(user_ids: List[int]):
    query = await __get_all_query()
    return query.join(DBUser).filter(DBUser.id.in_(user_ids))                    
                    

async def get_all_has_user_id(user_ids: List[int], db=Depends(get_db)) -> List[SchemaCommentLike]:
    query = await __get_all_query()
    query = query.join(DBUser).filter(DBUser.id.in_(user_ids))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_has_user_query(users: List[SchemaBaseUser]):
    query = await __get_all_query()
    return query.join(DBUser).filter(DBUser.id.in_(map(lambda x: x.id, users)))                    
                    

async def get_all_has_user(users: List[SchemaBaseUser], db=Depends(get_db)) -> List[SchemaCommentLike]:
    query = await __get_all_query()
    query = query.join(DBUser).filter(DBUser.id.in_(map(lambda x: x.id, users)))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_is_comment_id_query(comment_id: int):
    query = await __get_all_query()
    return query.join(DBComment).filter(DBComment.id.__eq__(comment_id))                    
                    

async def get_all_is_comment_id(comment_id: int, db=Depends(get_db)) -> List[SchemaCommentLike]:
    query = await __get_all_query()
    query = query.join(DBComment).filter(DBComment.id.__eq__(comment_id))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_is_comment_query(comment: SchemaBaseComment):
    query = await __get_all_query()
    return query.join(DBComment).filter(DBComment.id.__eq__(comment.id))                    
                    

async def get_all_is_comment(comment: SchemaBaseComment, db=Depends(get_db)) -> List[SchemaCommentLike]:
    query = await __get_all_query()
    query = query.join(DBComment).filter(DBComment.id.__eq__(comment.id))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_has_comment_id_query(comment_ids: List[int]):
    query = await __get_all_query()
    return query.join(DBComment).filter(DBComment.id.in_(comment_ids))                    
                    

async def get_all_has_comment_id(comment_ids: List[int], db=Depends(get_db)) -> List[SchemaCommentLike]:
    query = await __get_all_query()
    query = query.join(DBComment).filter(DBComment.id.in_(comment_ids))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_has_comment_query(comments: List[SchemaBaseComment]):
    query = await __get_all_query()
    return query.join(DBComment).filter(DBComment.id.in_(map(lambda x: x.id, comments)))                    
                    

async def get_all_has_comment(comments: List[SchemaBaseComment], db=Depends(get_db)) -> List[SchemaCommentLike]:
    query = await __get_all_query()
    query = query.join(DBComment).filter(DBComment.id.in_(map(lambda x: x.id, comments)))     
    return (await db.scalars(query)).all()                  
                    
