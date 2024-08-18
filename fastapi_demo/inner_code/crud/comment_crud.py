# generate_hash: 7dc81b0e39a3185d48a9f2ec9dbc8b26
"""
This file was automatically generated in 2024-08-18 15:51:57.931255
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
async def get_one(ident: int, db=Depends(get_db)) -> SchemaBaseComment:
    res = await db.get(DBComment, ident)
    if res and res.deleted_at is None:
        return res
    raise NOT_FOUND


async def batch_get(idents: List[int], db=Depends(get_db)) -> Page[SchemaBaseComment]:
    query = select(DBComment).filter(DBComment.deleted_at.is_(None)).filter(DBComment.id.in_(idents))
    return await paginate(db, query)


def get_all_query(
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
        query=Depends(get_all_query),
        db=Depends(get_db)
) -> Page[SchemaBaseComment]:
    return await paginate(db, query)


async def get_link_all(
        query=Depends(get_all_query),
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


def get_user_id_is_query(user_id: int) -> Select:
    query = get_all_query()
    query = query.join(DBUser).filter(DBUser.id.__eq__(user_id))
    query = query.options(joinedload(DBComment.user))
    query = query.options(joinedload(DBComment.post))
    query = query.options(selectinload(DBComment.likes))
    return query
                

async def get_user_id_is(user_id: int, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaComment]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBUser).filter(DBUser.id.__eq__(user_id))
    query = query.options(joinedload(DBComment.user))
    query = query.options(joinedload(DBComment.post))
    query = query.options(selectinload(DBComment.likes))
    return (await db.scalars(query)).all()
                

def get_user_is_query(user: SchemaBaseUser) -> Select:
    query = get_all_query()
    query = query.join(DBUser).filter(DBUser.id.__eq__(user.id))
    query = query.options(joinedload(DBComment.user))
    query = query.options(joinedload(DBComment.post))
    query = query.options(selectinload(DBComment.likes))
    return query
                

async def get_user_is(user: SchemaBaseUser, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaComment]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBUser).filter(DBUser.id.__eq__(user.id))
    query = query.options(joinedload(DBComment.user))
    query = query.options(joinedload(DBComment.post))
    query = query.options(selectinload(DBComment.likes))
    return (await db.scalars(query)).all()
                

def get_user_id_has_query(user_ids: List[int]) -> Select:
    query = get_all_query()
    query = query.join(DBUser).filter(DBUser.id.in_(user_ids))
    query = query.options(joinedload(DBComment.user))
    query = query.options(joinedload(DBComment.post))
    query = query.options(selectinload(DBComment.likes))
    return query
                

async def get_user_id_has(user_ids: List[int], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaComment]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBUser).filter(DBUser.id.in_(user_ids))
    query = query.options(joinedload(DBComment.user))
    query = query.options(joinedload(DBComment.post))
    query = query.options(selectinload(DBComment.likes))
    return (await db.scalars(query)).all()
                

def get_user_has_query(users: List[SchemaBaseUser]) -> Select:
    query = get_all_query()
    query = query.join(DBUser).filter(DBUser.id.in_(map(lambda x: x.id, users)))
    query = query.options(joinedload(DBComment.user))
    query = query.options(joinedload(DBComment.post))
    query = query.options(selectinload(DBComment.likes))
    return query
                

async def get_user_has(users: List[SchemaBaseUser], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaComment]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBUser).filter(DBUser.id.in_(map(lambda x: x.id, users)))
    query = query.options(joinedload(DBComment.user))
    query = query.options(joinedload(DBComment.post))
    query = query.options(selectinload(DBComment.likes))
    return (await db.scalars(query)).all()
                

def get_post_id_is_query(post_id: int) -> Select:
    query = get_all_query()
    query = query.join(DBPost).filter(DBPost.id.__eq__(post_id))
    query = query.options(joinedload(DBComment.user))
    query = query.options(joinedload(DBComment.post))
    query = query.options(selectinload(DBComment.likes))
    return query
                

async def get_post_id_is(post_id: int, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaComment]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBPost).filter(DBPost.id.__eq__(post_id))
    query = query.options(joinedload(DBComment.user))
    query = query.options(joinedload(DBComment.post))
    query = query.options(selectinload(DBComment.likes))
    return (await db.scalars(query)).all()
                

def get_post_is_query(post: SchemaBasePost) -> Select:
    query = get_all_query()
    query = query.join(DBPost).filter(DBPost.id.__eq__(post.id))
    query = query.options(joinedload(DBComment.user))
    query = query.options(joinedload(DBComment.post))
    query = query.options(selectinload(DBComment.likes))
    return query
                

async def get_post_is(post: SchemaBasePost, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaComment]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBPost).filter(DBPost.id.__eq__(post.id))
    query = query.options(joinedload(DBComment.user))
    query = query.options(joinedload(DBComment.post))
    query = query.options(selectinload(DBComment.likes))
    return (await db.scalars(query)).all()
                

def get_post_id_has_query(post_ids: List[int]) -> Select:
    query = get_all_query()
    query = query.join(DBPost).filter(DBPost.id.in_(post_ids))
    query = query.options(joinedload(DBComment.user))
    query = query.options(joinedload(DBComment.post))
    query = query.options(selectinload(DBComment.likes))
    return query
                

async def get_post_id_has(post_ids: List[int], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaComment]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBPost).filter(DBPost.id.in_(post_ids))
    query = query.options(joinedload(DBComment.user))
    query = query.options(joinedload(DBComment.post))
    query = query.options(selectinload(DBComment.likes))
    return (await db.scalars(query)).all()
                

def get_post_has_query(posts: List[SchemaBasePost]) -> Select:
    query = get_all_query()
    query = query.join(DBPost).filter(DBPost.id.in_(map(lambda x: x.id, posts)))
    query = query.options(joinedload(DBComment.user))
    query = query.options(joinedload(DBComment.post))
    query = query.options(selectinload(DBComment.likes))
    return query
                

async def get_post_has(posts: List[SchemaBasePost], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaComment]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBPost).filter(DBPost.id.in_(map(lambda x: x.id, posts)))
    query = query.options(joinedload(DBComment.user))
    query = query.options(joinedload(DBComment.post))
    query = query.options(selectinload(DBComment.likes))
    return (await db.scalars(query)).all()
                

def get_likes_id_is_query(comment_like_id: int) -> Select:
    query = get_all_query()
    query = query.join(DBCommentLike).filter(DBCommentLike.id.__eq__(comment_like_id))
    query = query.options(joinedload(DBComment.user))
    query = query.options(joinedload(DBComment.post))
    query = query.options(selectinload(DBComment.likes))
    return query
                

async def get_likes_id_is(comment_like_id: int, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaComment]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBCommentLike).filter(DBCommentLike.id.__eq__(comment_like_id))
    query = query.options(joinedload(DBComment.user))
    query = query.options(joinedload(DBComment.post))
    query = query.options(selectinload(DBComment.likes))
    return (await db.scalars(query)).all()
                

def get_likes_is_query(comment_like: SchemaBaseCommentLike) -> Select:
    query = get_all_query()
    query = query.join(DBCommentLike).filter(DBCommentLike.id.__eq__(comment_like.id))
    query = query.options(joinedload(DBComment.user))
    query = query.options(joinedload(DBComment.post))
    query = query.options(selectinload(DBComment.likes))
    return query
                

async def get_likes_is(comment_like: SchemaBaseCommentLike, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaComment]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBCommentLike).filter(DBCommentLike.id.__eq__(comment_like.id))
    query = query.options(joinedload(DBComment.user))
    query = query.options(joinedload(DBComment.post))
    query = query.options(selectinload(DBComment.likes))
    return (await db.scalars(query)).all()
                

def get_likes_id_has_query(comment_like_ids: List[int]) -> Select:
    query = get_all_query()
    query = query.join(DBCommentLike).filter(DBCommentLike.id.in_(comment_like_ids))
    query = query.options(joinedload(DBComment.user))
    query = query.options(joinedload(DBComment.post))
    query = query.options(selectinload(DBComment.likes))
    return query
                

async def get_likes_id_has(comment_like_ids: List[int], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaComment]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBCommentLike).filter(DBCommentLike.id.in_(comment_like_ids))
    query = query.options(joinedload(DBComment.user))
    query = query.options(joinedload(DBComment.post))
    query = query.options(selectinload(DBComment.likes))
    return (await db.scalars(query)).all()
                

def get_likes_has_query(comment_likes: List[SchemaBaseCommentLike]) -> Select:
    query = get_all_query()
    query = query.join(DBCommentLike).filter(DBCommentLike.id.in_(map(lambda x: x.id, comment_likes)))
    query = query.options(joinedload(DBComment.user))
    query = query.options(joinedload(DBComment.post))
    query = query.options(selectinload(DBComment.likes))
    return query
                

async def get_likes_has(comment_likes: List[SchemaBaseCommentLike], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaComment]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBCommentLike).filter(DBCommentLike.id.in_(map(lambda x: x.id, comment_likes)))
    query = query.options(joinedload(DBComment.user))
    query = query.options(joinedload(DBComment.post))
    query = query.options(selectinload(DBComment.likes))
    return (await db.scalars(query)).all()
                
