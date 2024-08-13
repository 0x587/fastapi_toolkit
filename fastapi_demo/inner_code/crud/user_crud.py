# generate_hash: b3c0bea5b552066b8bd1e5f55b7b3097
"""
This file was automatically generated in 2024-08-14 00:21:54.792501
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
async def get_one(ident: int, db=Depends(get_db)) -> SchemaBaseUser:
    res = await db.get(DBUser, ident)
    if res and res.deleted_at is None:
        return res
    raise NOT_FOUND


async def batch_get(idents: List[int], db=Depends(get_db)) -> Page[SchemaBaseUser]:
    query = select(DBUser).filter(DBUser.deleted_at.is_(None)).filter(DBUser.id.in_(idents))
    return await paginate(db, query)


async def __get_all_query(
        filter_name: Optional[str] = None,
        sort_by: Optional[str] = None, is_desc: bool = False,
) -> Select:
    query = select(DBUser).filter(DBUser.deleted_at.is_(None))
    if filter_name is not None:
        query = query.filter(DBUser.name.__eq__(filter_name))
    if sort_by is not None:
        if is_desc:
            query = query.order_by(getattr(DBUser, sort_by).desc())
        else:
            query = query.order_by(getattr(DBUser, sort_by))
    return query


async def get_all(
        query=Depends(__get_all_query),
        db=Depends(get_db)
) -> Page[SchemaBaseUser]:
    return await paginate(db, query)


async def get_link_all(
        query=Depends(__get_all_query),
        db=Depends(get_db)
) -> Page[SchemaUser]:
    return await paginate(db, query)
# ---------------------User Query Routes----------------------


# -----------------------Create Routes------------------------
async def create_one(
        name: str,
        db=Depends(get_db)
) -> SchemaBaseUser:
    user = SchemaBaseUser(
        name=name,
    )
    user = DBUser(**user.model_dump())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return SchemaBaseUser.model_validate(user)


# -----------------------Update Routes------------------------
async def update_one(
        ident: int,
        name: Optional[str] = None,
        db=Depends(get_db)) -> SchemaBaseUser:
    res = await db.get(DBUser, ident)
    if not res or res.deleted_at is not None:
        raise NOT_FOUND
    if name is not None:
        res.name = name
    res.updated_at = datetime.datetime.now()
    await db.commit()
    await db.refresh(res)
    return SchemaBaseUser.model_validate(res)


# -----------------------Delete Routes------------------------
async def delete_one(ident: int, db=Depends(get_db)):
    res = await db.get(DBUser, ident)
    if not res or res.deleted_at is not None:
        raise NOT_FOUND
# TODO
    res.deleted_at = datetime.datetime.now()
    await db.commit()
    return {'message': 'Deleted', 'id': ident}


# ----------------------Relation Routes-----------------------


async def get_all_is_posts_id_query(post_id: int):
    query = await __get_all_query()
    return query.join(DBPost).filter(DBPost.id.__eq__(post_id))                    
                    

async def get_all_is_posts_id(post_id: int, db=Depends(get_db)) -> List[SchemaUser]:
    query = await __get_all_query()
    query = query.join(DBPost).filter(DBPost.id.__eq__(post_id))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_is_posts_query(post: SchemaBasePost):
    query = await __get_all_query()
    return query.join(DBPost).filter(DBPost.id.__eq__(post.id))                    
                    

async def get_all_is_posts(post: SchemaBasePost, db=Depends(get_db)) -> List[SchemaUser]:
    query = await __get_all_query()
    query = query.join(DBPost).filter(DBPost.id.__eq__(post.id))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_has_posts_id_query(post_ids: List[int]):
    query = await __get_all_query()
    return query.join(DBPost).filter(DBPost.id.in_(post_ids))                    
                    

async def get_all_has_posts_id(post_ids: List[int], db=Depends(get_db)) -> List[SchemaUser]:
    query = await __get_all_query()
    query = query.join(DBPost).filter(DBPost.id.in_(post_ids))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_has_posts_query(posts: List[SchemaBasePost]):
    query = await __get_all_query()
    return query.join(DBPost).filter(DBPost.id.in_(map(lambda x: x.id, posts)))                    
                    

async def get_all_has_posts(posts: List[SchemaBasePost], db=Depends(get_db)) -> List[SchemaUser]:
    query = await __get_all_query()
    query = query.join(DBPost).filter(DBPost.id.in_(map(lambda x: x.id, posts)))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_is_comments_id_query(comment_id: int):
    query = await __get_all_query()
    return query.join(DBComment).filter(DBComment.id.__eq__(comment_id))                    
                    

async def get_all_is_comments_id(comment_id: int, db=Depends(get_db)) -> List[SchemaUser]:
    query = await __get_all_query()
    query = query.join(DBComment).filter(DBComment.id.__eq__(comment_id))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_is_comments_query(comment: SchemaBaseComment):
    query = await __get_all_query()
    return query.join(DBComment).filter(DBComment.id.__eq__(comment.id))                    
                    

async def get_all_is_comments(comment: SchemaBaseComment, db=Depends(get_db)) -> List[SchemaUser]:
    query = await __get_all_query()
    query = query.join(DBComment).filter(DBComment.id.__eq__(comment.id))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_has_comments_id_query(comment_ids: List[int]):
    query = await __get_all_query()
    return query.join(DBComment).filter(DBComment.id.in_(comment_ids))                    
                    

async def get_all_has_comments_id(comment_ids: List[int], db=Depends(get_db)) -> List[SchemaUser]:
    query = await __get_all_query()
    query = query.join(DBComment).filter(DBComment.id.in_(comment_ids))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_has_comments_query(comments: List[SchemaBaseComment]):
    query = await __get_all_query()
    return query.join(DBComment).filter(DBComment.id.in_(map(lambda x: x.id, comments)))                    
                    

async def get_all_has_comments(comments: List[SchemaBaseComment], db=Depends(get_db)) -> List[SchemaUser]:
    query = await __get_all_query()
    query = query.join(DBComment).filter(DBComment.id.in_(map(lambda x: x.id, comments)))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_is_post_likes_id_query(post_like_id: int):
    query = await __get_all_query()
    return query.join(DBPostLike).filter(DBPostLike.id.__eq__(post_like_id))                    
                    

async def get_all_is_post_likes_id(post_like_id: int, db=Depends(get_db)) -> List[SchemaUser]:
    query = await __get_all_query()
    query = query.join(DBPostLike).filter(DBPostLike.id.__eq__(post_like_id))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_is_post_likes_query(post_like: SchemaBasePostLike):
    query = await __get_all_query()
    return query.join(DBPostLike).filter(DBPostLike.id.__eq__(post_like.id))                    
                    

async def get_all_is_post_likes(post_like: SchemaBasePostLike, db=Depends(get_db)) -> List[SchemaUser]:
    query = await __get_all_query()
    query = query.join(DBPostLike).filter(DBPostLike.id.__eq__(post_like.id))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_has_post_likes_id_query(post_like_ids: List[int]):
    query = await __get_all_query()
    return query.join(DBPostLike).filter(DBPostLike.id.in_(post_like_ids))                    
                    

async def get_all_has_post_likes_id(post_like_ids: List[int], db=Depends(get_db)) -> List[SchemaUser]:
    query = await __get_all_query()
    query = query.join(DBPostLike).filter(DBPostLike.id.in_(post_like_ids))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_has_post_likes_query(post_likes: List[SchemaBasePostLike]):
    query = await __get_all_query()
    return query.join(DBPostLike).filter(DBPostLike.id.in_(map(lambda x: x.id, post_likes)))                    
                    

async def get_all_has_post_likes(post_likes: List[SchemaBasePostLike], db=Depends(get_db)) -> List[SchemaUser]:
    query = await __get_all_query()
    query = query.join(DBPostLike).filter(DBPostLike.id.in_(map(lambda x: x.id, post_likes)))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_is_comment_likes_id_query(comment_like_id: int):
    query = await __get_all_query()
    return query.join(DBCommentLike).filter(DBCommentLike.id.__eq__(comment_like_id))                    
                    

async def get_all_is_comment_likes_id(comment_like_id: int, db=Depends(get_db)) -> List[SchemaUser]:
    query = await __get_all_query()
    query = query.join(DBCommentLike).filter(DBCommentLike.id.__eq__(comment_like_id))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_is_comment_likes_query(comment_like: SchemaBaseCommentLike):
    query = await __get_all_query()
    return query.join(DBCommentLike).filter(DBCommentLike.id.__eq__(comment_like.id))                    
                    

async def get_all_is_comment_likes(comment_like: SchemaBaseCommentLike, db=Depends(get_db)) -> List[SchemaUser]:
    query = await __get_all_query()
    query = query.join(DBCommentLike).filter(DBCommentLike.id.__eq__(comment_like.id))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_has_comment_likes_id_query(comment_like_ids: List[int]):
    query = await __get_all_query()
    return query.join(DBCommentLike).filter(DBCommentLike.id.in_(comment_like_ids))                    
                    

async def get_all_has_comment_likes_id(comment_like_ids: List[int], db=Depends(get_db)) -> List[SchemaUser]:
    query = await __get_all_query()
    query = query.join(DBCommentLike).filter(DBCommentLike.id.in_(comment_like_ids))     
    return (await db.scalars(query)).all()                  
                    

async def get_all_has_comment_likes_query(comment_likes: List[SchemaBaseCommentLike]):
    query = await __get_all_query()
    return query.join(DBCommentLike).filter(DBCommentLike.id.in_(map(lambda x: x.id, comment_likes)))                    
                    

async def get_all_has_comment_likes(comment_likes: List[SchemaBaseCommentLike], db=Depends(get_db)) -> List[SchemaUser]:
    query = await __get_all_query()
    query = query.join(DBCommentLike).filter(DBCommentLike.id.in_(map(lambda x: x.id, comment_likes)))     
    return (await db.scalars(query)).all()                  
                    
