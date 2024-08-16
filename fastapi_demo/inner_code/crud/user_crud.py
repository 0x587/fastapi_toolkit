# generate_hash: 21ca5e4d895ba1d0e1d6b806de27106a
"""
This file was automatically generated in 2024-08-16 23:39:27.967310
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
async def get_one(ident: int, db=Depends(get_db)) -> SchemaBaseUser:
    res = await db.get(DBUser, ident)
    if res and res.deleted_at is None:
        return res
    raise NOT_FOUND


async def batch_get(idents: List[int], db=Depends(get_db)) -> Page[SchemaBaseUser]:
    query = select(DBUser).filter(DBUser.deleted_at.is_(None)).filter(DBUser.id.in_(idents))
    return await paginate(db, query)


async def get_all_query(
        filter_name: Optional[str] = None,
        filter_user_key: Optional[str] = None,
        sort_by: Optional[str] = None, is_desc: bool = False,
) -> Select:
    query = select(DBUser).filter(DBUser.deleted_at.is_(None))
    if filter_name is not None:
        query = query.filter(DBUser.name.__eq__(filter_name))
    if filter_user_key is not None:
        query = query.filter(DBUser.user_key.__eq__(filter_user_key))
    if sort_by is not None:
        if is_desc:
            query = query.order_by(getattr(DBUser, sort_by).desc())
        else:
            query = query.order_by(getattr(DBUser, sort_by))
    return query


async def get_all(
        query=Depends(get_all_query),
        db=Depends(get_db)
) -> Page[SchemaBaseUser]:
    return await paginate(db, query)


async def get_link_all(
        query=Depends(get_all_query),
        db=Depends(get_db)
) -> Page[SchemaUser]:
    return await paginate(db, query)
# ---------------------User Query Routes----------------------


# -----------------------Create Routes------------------------
async def create_one(
        name: str,
        user_key: str,
        db=Depends(get_db)
) -> SchemaBaseUser:
    user = SchemaBaseUser(
        name=name,
        user_key=user_key,
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
        user_key: Optional[str] = None,
        db=Depends(get_db)) -> SchemaBaseUser:
    res = await db.get(DBUser, ident)
    if not res or res.deleted_at is not None:
        raise NOT_FOUND
    if name is not None:
        res.name = name
    if user_key is not None:
        res.user_key = user_key
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


async def get_all_is_posts_id(post_id: int, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaUser]:
    if type(query) is not Select:
        query = await get_all_query()
    query = query.join(DBPost).filter(DBPost.id.__eq__(post_id))
    query = query.options(selectinload(DBUser.posts))
    query = query.options(selectinload(DBUser.comments))
    query = query.options(selectinload(DBUser.post_likes))
    query = query.options(selectinload(DBUser.comment_likes))
    return (await db.scalars(query)).all()
                

async def get_all_is_posts(post: SchemaBasePost, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaUser]:
    if type(query) is not Select:
        query = await get_all_query()
    query = query.join(DBPost).filter(DBPost.id.__eq__(post.id))
    query = query.options(selectinload(DBUser.posts))
    query = query.options(selectinload(DBUser.comments))
    query = query.options(selectinload(DBUser.post_likes))
    query = query.options(selectinload(DBUser.comment_likes))
    return (await db.scalars(query)).all()
                

async def get_all_has_posts_id(post_ids: List[int], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaUser]:
    if type(query) is not Select:
        query = await get_all_query()
    query = query.join(DBPost).filter(DBPost.id.in_(post_ids))
    query = query.options(selectinload(DBUser.posts))
    query = query.options(selectinload(DBUser.comments))
    query = query.options(selectinload(DBUser.post_likes))
    query = query.options(selectinload(DBUser.comment_likes))
    return (await db.scalars(query)).all()
                

async def get_all_has_posts(posts: List[SchemaBasePost], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaUser]:
    if type(query) is not Select:
        query = await get_all_query()
    query = query.join(DBPost).filter(DBPost.id.in_(map(lambda x: x.id, posts)))
    query = query.options(selectinload(DBUser.posts))
    query = query.options(selectinload(DBUser.comments))
    query = query.options(selectinload(DBUser.post_likes))
    query = query.options(selectinload(DBUser.comment_likes))
    return (await db.scalars(query)).all()
                

async def get_all_is_comments_id(comment_id: int, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaUser]:
    if type(query) is not Select:
        query = await get_all_query()
    query = query.join(DBComment).filter(DBComment.id.__eq__(comment_id))
    query = query.options(selectinload(DBUser.posts))
    query = query.options(selectinload(DBUser.comments))
    query = query.options(selectinload(DBUser.post_likes))
    query = query.options(selectinload(DBUser.comment_likes))
    return (await db.scalars(query)).all()
                

async def get_all_is_comments(comment: SchemaBaseComment, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaUser]:
    if type(query) is not Select:
        query = await get_all_query()
    query = query.join(DBComment).filter(DBComment.id.__eq__(comment.id))
    query = query.options(selectinload(DBUser.posts))
    query = query.options(selectinload(DBUser.comments))
    query = query.options(selectinload(DBUser.post_likes))
    query = query.options(selectinload(DBUser.comment_likes))
    return (await db.scalars(query)).all()
                

async def get_all_has_comments_id(comment_ids: List[int], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaUser]:
    if type(query) is not Select:
        query = await get_all_query()
    query = query.join(DBComment).filter(DBComment.id.in_(comment_ids))
    query = query.options(selectinload(DBUser.posts))
    query = query.options(selectinload(DBUser.comments))
    query = query.options(selectinload(DBUser.post_likes))
    query = query.options(selectinload(DBUser.comment_likes))
    return (await db.scalars(query)).all()
                

async def get_all_has_comments(comments: List[SchemaBaseComment], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaUser]:
    if type(query) is not Select:
        query = await get_all_query()
    query = query.join(DBComment).filter(DBComment.id.in_(map(lambda x: x.id, comments)))
    query = query.options(selectinload(DBUser.posts))
    query = query.options(selectinload(DBUser.comments))
    query = query.options(selectinload(DBUser.post_likes))
    query = query.options(selectinload(DBUser.comment_likes))
    return (await db.scalars(query)).all()
                

async def get_all_is_post_likes_id(post_like_id: int, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaUser]:
    if type(query) is not Select:
        query = await get_all_query()
    query = query.join(DBPostLike).filter(DBPostLike.id.__eq__(post_like_id))
    query = query.options(selectinload(DBUser.posts))
    query = query.options(selectinload(DBUser.comments))
    query = query.options(selectinload(DBUser.post_likes))
    query = query.options(selectinload(DBUser.comment_likes))
    return (await db.scalars(query)).all()
                

async def get_all_is_post_likes(post_like: SchemaBasePostLike, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaUser]:
    if type(query) is not Select:
        query = await get_all_query()
    query = query.join(DBPostLike).filter(DBPostLike.id.__eq__(post_like.id))
    query = query.options(selectinload(DBUser.posts))
    query = query.options(selectinload(DBUser.comments))
    query = query.options(selectinload(DBUser.post_likes))
    query = query.options(selectinload(DBUser.comment_likes))
    return (await db.scalars(query)).all()
                

async def get_all_has_post_likes_id(post_like_ids: List[int], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaUser]:
    if type(query) is not Select:
        query = await get_all_query()
    query = query.join(DBPostLike).filter(DBPostLike.id.in_(post_like_ids))
    query = query.options(selectinload(DBUser.posts))
    query = query.options(selectinload(DBUser.comments))
    query = query.options(selectinload(DBUser.post_likes))
    query = query.options(selectinload(DBUser.comment_likes))
    return (await db.scalars(query)).all()
                

async def get_all_has_post_likes(post_likes: List[SchemaBasePostLike], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaUser]:
    if type(query) is not Select:
        query = await get_all_query()
    query = query.join(DBPostLike).filter(DBPostLike.id.in_(map(lambda x: x.id, post_likes)))
    query = query.options(selectinload(DBUser.posts))
    query = query.options(selectinload(DBUser.comments))
    query = query.options(selectinload(DBUser.post_likes))
    query = query.options(selectinload(DBUser.comment_likes))
    return (await db.scalars(query)).all()
                

async def get_all_is_comment_likes_id(comment_like_id: int, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaUser]:
    if type(query) is not Select:
        query = await get_all_query()
    query = query.join(DBCommentLike).filter(DBCommentLike.id.__eq__(comment_like_id))
    query = query.options(selectinload(DBUser.posts))
    query = query.options(selectinload(DBUser.comments))
    query = query.options(selectinload(DBUser.post_likes))
    query = query.options(selectinload(DBUser.comment_likes))
    return (await db.scalars(query)).all()
                

async def get_all_is_comment_likes(comment_like: SchemaBaseCommentLike, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaUser]:
    if type(query) is not Select:
        query = await get_all_query()
    query = query.join(DBCommentLike).filter(DBCommentLike.id.__eq__(comment_like.id))
    query = query.options(selectinload(DBUser.posts))
    query = query.options(selectinload(DBUser.comments))
    query = query.options(selectinload(DBUser.post_likes))
    query = query.options(selectinload(DBUser.comment_likes))
    return (await db.scalars(query)).all()
                

async def get_all_has_comment_likes_id(comment_like_ids: List[int], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaUser]:
    if type(query) is not Select:
        query = await get_all_query()
    query = query.join(DBCommentLike).filter(DBCommentLike.id.in_(comment_like_ids))
    query = query.options(selectinload(DBUser.posts))
    query = query.options(selectinload(DBUser.comments))
    query = query.options(selectinload(DBUser.post_likes))
    query = query.options(selectinload(DBUser.comment_likes))
    return (await db.scalars(query)).all()
                

async def get_all_has_comment_likes(comment_likes: List[SchemaBaseCommentLike], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaUser]:
    if type(query) is not Select:
        query = await get_all_query()
    query = query.join(DBCommentLike).filter(DBCommentLike.id.in_(map(lambda x: x.id, comment_likes)))
    query = query.options(selectinload(DBUser.posts))
    query = query.options(selectinload(DBUser.comments))
    query = query.options(selectinload(DBUser.post_likes))
    query = query.options(selectinload(DBUser.comment_likes))
    return (await db.scalars(query)).all()
                
