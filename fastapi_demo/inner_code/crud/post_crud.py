# generate_hash: d460b22feca2161d20cd0891d1d84d1d
"""
This file was automatically generated in 2024-08-14 00:21:54.794044
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
async def get_one(ident: int, db=Depends(get_db)) -> SchemaBasePost:
    res = await db.get(DBPost, ident)
    if res and res.deleted_at is None:
        return res
    raise NOT_FOUND


async def batch_get(idents: List[int], db=Depends(get_db)) -> Page[SchemaBasePost]:
    query = select(DBPost).filter(DBPost.deleted_at.is_(None)).filter(DBPost.id.in_(idents))
    return await paginate(db, query)


async def __get_all_query(
        filter_text: Optional[str] = None,
        sort_by: Optional[str] = None, is_desc: bool = False,
) -> Select:
    query = select(DBPost).filter(DBPost.deleted_at.is_(None))
    if filter_text is not None:
        query = query.filter(DBPost.text.__eq__(filter_text))
    if sort_by is not None:
        if is_desc:
            query = query.order_by(getattr(DBPost, sort_by).desc())
        else:
            query = query.order_by(getattr(DBPost, sort_by))
    return query


async def get_all(
        query=Depends(__get_all_query),
        db=Depends(get_db)
) -> Page[SchemaBasePost]:
    return await paginate(db, query)


async def get_link_all(
        query=Depends(__get_all_query),
        db=Depends(get_db)
) -> Page[SchemaPost]:
    return await paginate(db, query)
# ---------------------User Query Routes----------------------


# -----------------------Create Routes------------------------
async def create_one(
        text: str,
        db=Depends(get_db)
) -> SchemaBasePost:
    post = SchemaBasePost(
        text=text,
    )
    post = DBPost(**post.model_dump())
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return SchemaBasePost.model_validate(post)


# -----------------------Update Routes------------------------
async def update_one(
        ident: int,
        text: Optional[str] = None,
        db=Depends(get_db)) -> SchemaBasePost:
    res = await db.get(DBPost, ident)
    if not res or res.deleted_at is not None:
        raise NOT_FOUND
    if text is not None:
        res.text = text
    res.updated_at = datetime.datetime.now()
    await db.commit()
    await db.refresh(res)
    return SchemaBasePost.model_validate(res)


# -----------------------Delete Routes------------------------
async def delete_one(ident: int, db=Depends(get_db)):
    res = await db.get(DBPost, ident)
    if not res or res.deleted_at is not None:
        raise NOT_FOUND
# TODO
    res.deleted_at = datetime.datetime.now()
    await db.commit()
    return {'message': 'Deleted', 'id': ident}


# ----------------------Relation Routes-----------------------


async def get_all_is_author_id_query(user_id: int):
    query = await __get_all_query()
    return query.join(DBUser).filter(DBUser.id.__eq__(user_id))                    
                    

async def get_all_is_author_id(user_id: int, db=Depends(get_db)) -> List[SchemaPost]:
    query = await __get_all_query()
    query = query.join(DBUser).filter(DBUser.id.__eq__(user_id))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_is_author_query(user: SchemaBaseUser):
    query = await __get_all_query()
    return query.join(DBUser).filter(DBUser.id.__eq__(user.id))                    
                    

async def get_all_is_author(user: SchemaBaseUser, db=Depends(get_db)) -> List[SchemaPost]:
    query = await __get_all_query()
    query = query.join(DBUser).filter(DBUser.id.__eq__(user.id))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_has_author_id_query(user_ids: List[int]):
    query = await __get_all_query()
    return query.join(DBUser).filter(DBUser.id.in_(user_ids))                    
                    

async def get_all_has_author_id(user_ids: List[int], db=Depends(get_db)) -> List[SchemaPost]:
    query = await __get_all_query()
    query = query.join(DBUser).filter(DBUser.id.in_(user_ids))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_has_author_query(users: List[SchemaBaseUser]):
    query = await __get_all_query()
    return query.join(DBUser).filter(DBUser.id.in_(map(lambda x: x.id, users)))                    
                    

async def get_all_has_author(users: List[SchemaBaseUser], db=Depends(get_db)) -> List[SchemaPost]:
    query = await __get_all_query()
    query = query.join(DBUser).filter(DBUser.id.in_(map(lambda x: x.id, users)))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_is_comments_id_query(comment_id: int):
    query = await __get_all_query()
    return query.join(DBComment).filter(DBComment.id.__eq__(comment_id))                    
                    

async def get_all_is_comments_id(comment_id: int, db=Depends(get_db)) -> List[SchemaPost]:
    query = await __get_all_query()
    query = query.join(DBComment).filter(DBComment.id.__eq__(comment_id))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_is_comments_query(comment: SchemaBaseComment):
    query = await __get_all_query()
    return query.join(DBComment).filter(DBComment.id.__eq__(comment.id))                    
                    

async def get_all_is_comments(comment: SchemaBaseComment, db=Depends(get_db)) -> List[SchemaPost]:
    query = await __get_all_query()
    query = query.join(DBComment).filter(DBComment.id.__eq__(comment.id))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_has_comments_id_query(comment_ids: List[int]):
    query = await __get_all_query()
    return query.join(DBComment).filter(DBComment.id.in_(comment_ids))                    
                    

async def get_all_has_comments_id(comment_ids: List[int], db=Depends(get_db)) -> List[SchemaPost]:
    query = await __get_all_query()
    query = query.join(DBComment).filter(DBComment.id.in_(comment_ids))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_has_comments_query(comments: List[SchemaBaseComment]):
    query = await __get_all_query()
    return query.join(DBComment).filter(DBComment.id.in_(map(lambda x: x.id, comments)))                    
                    

async def get_all_has_comments(comments: List[SchemaBaseComment], db=Depends(get_db)) -> List[SchemaPost]:
    query = await __get_all_query()
    query = query.join(DBComment).filter(DBComment.id.in_(map(lambda x: x.id, comments)))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_is_likes_id_query(post_like_id: int):
    query = await __get_all_query()
    return query.join(DBPostLike).filter(DBPostLike.id.__eq__(post_like_id))                    
                    

async def get_all_is_likes_id(post_like_id: int, db=Depends(get_db)) -> List[SchemaPost]:
    query = await __get_all_query()
    query = query.join(DBPostLike).filter(DBPostLike.id.__eq__(post_like_id))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_is_likes_query(post_like: SchemaBasePostLike):
    query = await __get_all_query()
    return query.join(DBPostLike).filter(DBPostLike.id.__eq__(post_like.id))                    
                    

async def get_all_is_likes(post_like: SchemaBasePostLike, db=Depends(get_db)) -> List[SchemaPost]:
    query = await __get_all_query()
    query = query.join(DBPostLike).filter(DBPostLike.id.__eq__(post_like.id))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_has_likes_id_query(post_like_ids: List[int]):
    query = await __get_all_query()
    return query.join(DBPostLike).filter(DBPostLike.id.in_(post_like_ids))                    
                    

async def get_all_has_likes_id(post_like_ids: List[int], db=Depends(get_db)) -> List[SchemaPost]:
    query = await __get_all_query()
    query = query.join(DBPostLike).filter(DBPostLike.id.in_(post_like_ids))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_has_likes_query(post_likes: List[SchemaBasePostLike]):
    query = await __get_all_query()
    return query.join(DBPostLike).filter(DBPostLike.id.in_(map(lambda x: x.id, post_likes)))                    
                    

async def get_all_has_likes(post_likes: List[SchemaBasePostLike], db=Depends(get_db)) -> List[SchemaPost]:
    query = await __get_all_query()
    query = query.join(DBPostLike).filter(DBPostLike.id.in_(map(lambda x: x.id, post_likes)))     
    return (await db.scalars(query)).all()                  
                    
