# generate_hash: 8f549246a4b467e0e4073df9f6f284e5
"""
This file was automatically generated in 2024-08-14 00:21:54.794431
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
async def get_one(ident: int, db=Depends(get_db)) -> SchemaBaseComment:
    res = await db.get(DBComment, ident)
    if res and res.deleted_at is None:
        return res
    raise NOT_FOUND


async def batch_get(idents: List[int], db=Depends(get_db)) -> Page[SchemaBaseComment]:
    query = select(DBComment).filter(DBComment.deleted_at.is_(None)).filter(DBComment.id.in_(idents))
    return await paginate(db, query)


async def __get_all_query(
        filter_content: Optional[str] = None,
        sort_by: Optional[str] = None, is_desc: bool = False,
) -> Select:
    query = select(DBComment).filter(DBComment.deleted_at.is_(None))
    if filter_content is not None:
        query = query.filter(DBComment.content.__eq__(filter_content))
    if sort_by is not None:
        if is_desc:
            query = query.order_by(getattr(DBComment, sort_by).desc())
        else:
            query = query.order_by(getattr(DBComment, sort_by))
    return query


async def get_all(
        query=Depends(__get_all_query),
        db=Depends(get_db)
) -> Page[SchemaBaseComment]:
    return await paginate(db, query)


async def get_link_all(
        query=Depends(__get_all_query),
        db=Depends(get_db)
) -> Page[SchemaComment]:
    return await paginate(db, query)
# ---------------------User Query Routes----------------------


# -----------------------Create Routes------------------------
async def create_one(
        content: str,
        db=Depends(get_db)
) -> SchemaBaseComment:
    comment = SchemaBaseComment(
        content=content,
    )
    comment = DBComment(**comment.model_dump())
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return SchemaBaseComment.model_validate(comment)


# -----------------------Update Routes------------------------
async def update_one(
        ident: int,
        content: Optional[str] = None,
        db=Depends(get_db)) -> SchemaBaseComment:
    res = await db.get(DBComment, ident)
    if not res or res.deleted_at is not None:
        raise NOT_FOUND
    if content is not None:
        res.content = content
    res.updated_at = datetime.datetime.now()
    await db.commit()
    await db.refresh(res)
    return SchemaBaseComment.model_validate(res)


# -----------------------Delete Routes------------------------
async def delete_one(ident: int, db=Depends(get_db)):
    res = await db.get(DBComment, ident)
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
                    

async def get_all_is_user_id(user_id: int, db=Depends(get_db)) -> List[SchemaComment]:
    query = await __get_all_query()
    query = query.join(DBUser).filter(DBUser.id.__eq__(user_id))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_is_user_query(user: SchemaBaseUser):
    query = await __get_all_query()
    return query.join(DBUser).filter(DBUser.id.__eq__(user.id))                    
                    

async def get_all_is_user(user: SchemaBaseUser, db=Depends(get_db)) -> List[SchemaComment]:
    query = await __get_all_query()
    query = query.join(DBUser).filter(DBUser.id.__eq__(user.id))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_has_user_id_query(user_ids: List[int]):
    query = await __get_all_query()
    return query.join(DBUser).filter(DBUser.id.in_(user_ids))                    
                    

async def get_all_has_user_id(user_ids: List[int], db=Depends(get_db)) -> List[SchemaComment]:
    query = await __get_all_query()
    query = query.join(DBUser).filter(DBUser.id.in_(user_ids))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_has_user_query(users: List[SchemaBaseUser]):
    query = await __get_all_query()
    return query.join(DBUser).filter(DBUser.id.in_(map(lambda x: x.id, users)))                    
                    

async def get_all_has_user(users: List[SchemaBaseUser], db=Depends(get_db)) -> List[SchemaComment]:
    query = await __get_all_query()
    query = query.join(DBUser).filter(DBUser.id.in_(map(lambda x: x.id, users)))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_is_post_id_query(post_id: int):
    query = await __get_all_query()
    return query.join(DBPost).filter(DBPost.id.__eq__(post_id))                    
                    

async def get_all_is_post_id(post_id: int, db=Depends(get_db)) -> List[SchemaComment]:
    query = await __get_all_query()
    query = query.join(DBPost).filter(DBPost.id.__eq__(post_id))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_is_post_query(post: SchemaBasePost):
    query = await __get_all_query()
    return query.join(DBPost).filter(DBPost.id.__eq__(post.id))                    
                    

async def get_all_is_post(post: SchemaBasePost, db=Depends(get_db)) -> List[SchemaComment]:
    query = await __get_all_query()
    query = query.join(DBPost).filter(DBPost.id.__eq__(post.id))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_has_post_id_query(post_ids: List[int]):
    query = await __get_all_query()
    return query.join(DBPost).filter(DBPost.id.in_(post_ids))                    
                    

async def get_all_has_post_id(post_ids: List[int], db=Depends(get_db)) -> List[SchemaComment]:
    query = await __get_all_query()
    query = query.join(DBPost).filter(DBPost.id.in_(post_ids))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_has_post_query(posts: List[SchemaBasePost]):
    query = await __get_all_query()
    return query.join(DBPost).filter(DBPost.id.in_(map(lambda x: x.id, posts)))                    
                    

async def get_all_has_post(posts: List[SchemaBasePost], db=Depends(get_db)) -> List[SchemaComment]:
    query = await __get_all_query()
    query = query.join(DBPost).filter(DBPost.id.in_(map(lambda x: x.id, posts)))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_is_likes_id_query(comment_like_id: int):
    query = await __get_all_query()
    return query.join(DBCommentLike).filter(DBCommentLike.id.__eq__(comment_like_id))                    
                    

async def get_all_is_likes_id(comment_like_id: int, db=Depends(get_db)) -> List[SchemaComment]:
    query = await __get_all_query()
    query = query.join(DBCommentLike).filter(DBCommentLike.id.__eq__(comment_like_id))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_is_likes_query(comment_like: SchemaBaseCommentLike):
    query = await __get_all_query()
    return query.join(DBCommentLike).filter(DBCommentLike.id.__eq__(comment_like.id))                    
                    

async def get_all_is_likes(comment_like: SchemaBaseCommentLike, db=Depends(get_db)) -> List[SchemaComment]:
    query = await __get_all_query()
    query = query.join(DBCommentLike).filter(DBCommentLike.id.__eq__(comment_like.id))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_has_likes_id_query(comment_like_ids: List[int]):
    query = await __get_all_query()
    return query.join(DBCommentLike).filter(DBCommentLike.id.in_(comment_like_ids))                    
                    

async def get_all_has_likes_id(comment_like_ids: List[int], db=Depends(get_db)) -> List[SchemaComment]:
    query = await __get_all_query()
    query = query.join(DBCommentLike).filter(DBCommentLike.id.in_(comment_like_ids))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_has_likes_query(comment_likes: List[SchemaBaseCommentLike]):
    query = await __get_all_query()
    return query.join(DBCommentLike).filter(DBCommentLike.id.in_(map(lambda x: x.id, comment_likes)))                    
                    

async def get_all_has_likes(comment_likes: List[SchemaBaseCommentLike], db=Depends(get_db)) -> List[SchemaComment]:
    query = await __get_all_query()
    query = query.join(DBCommentLike).filter(DBCommentLike.id.in_(map(lambda x: x.id, comment_likes)))     
    return (await db.scalars(query)).all()                  
                    
