# generate_hash: e43221aaf97b4d422142d7268997f329
"""
This file was automatically generated in 2024-08-18 15:51:57.930581
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
async def get_one(ident: int, db=Depends(get_db)) -> SchemaBasePost:
    res = await db.get(DBPost, ident)
    if res and res.deleted_at is None:
        return res
    raise NOT_FOUND


async def batch_get(idents: List[int], db=Depends(get_db)) -> Page[SchemaBasePost]:
    query = select(DBPost).filter(DBPost.deleted_at.is_(None)).filter(DBPost.id.in_(idents))
    return await paginate(db, query)


def get_all_query(
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
        query=Depends(get_all_query),
        db=Depends(get_db)
) -> Page[SchemaBasePost]:
    return await paginate(db, query)


async def get_link_all(
        query=Depends(get_all_query),
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


def get_author_id_is_query(user_id: int) -> Select:
    query = get_all_query()
    query = query.join(DBUser).filter(DBUser.id.__eq__(user_id))
    query = query.options(joinedload(DBPost.author))
    query = query.options(selectinload(DBPost.comments))
    query = query.options(selectinload(DBPost.likes))
    return query
                

async def get_author_id_is(user_id: int, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaPost]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBUser).filter(DBUser.id.__eq__(user_id))
    query = query.options(joinedload(DBPost.author))
    query = query.options(selectinload(DBPost.comments))
    query = query.options(selectinload(DBPost.likes))
    return (await db.scalars(query)).all()
                

def get_author_is_query(user: SchemaBaseUser) -> Select:
    query = get_all_query()
    query = query.join(DBUser).filter(DBUser.id.__eq__(user.id))
    query = query.options(joinedload(DBPost.author))
    query = query.options(selectinload(DBPost.comments))
    query = query.options(selectinload(DBPost.likes))
    return query
                

async def get_author_is(user: SchemaBaseUser, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaPost]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBUser).filter(DBUser.id.__eq__(user.id))
    query = query.options(joinedload(DBPost.author))
    query = query.options(selectinload(DBPost.comments))
    query = query.options(selectinload(DBPost.likes))
    return (await db.scalars(query)).all()
                

def get_author_id_has_query(user_ids: List[int]) -> Select:
    query = get_all_query()
    query = query.join(DBUser).filter(DBUser.id.in_(user_ids))
    query = query.options(joinedload(DBPost.author))
    query = query.options(selectinload(DBPost.comments))
    query = query.options(selectinload(DBPost.likes))
    return query
                

async def get_author_id_has(user_ids: List[int], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaPost]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBUser).filter(DBUser.id.in_(user_ids))
    query = query.options(joinedload(DBPost.author))
    query = query.options(selectinload(DBPost.comments))
    query = query.options(selectinload(DBPost.likes))
    return (await db.scalars(query)).all()
                

def get_author_has_query(users: List[SchemaBaseUser]) -> Select:
    query = get_all_query()
    query = query.join(DBUser).filter(DBUser.id.in_(map(lambda x: x.id, users)))
    query = query.options(joinedload(DBPost.author))
    query = query.options(selectinload(DBPost.comments))
    query = query.options(selectinload(DBPost.likes))
    return query
                

async def get_author_has(users: List[SchemaBaseUser], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaPost]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBUser).filter(DBUser.id.in_(map(lambda x: x.id, users)))
    query = query.options(joinedload(DBPost.author))
    query = query.options(selectinload(DBPost.comments))
    query = query.options(selectinload(DBPost.likes))
    return (await db.scalars(query)).all()
                

def get_comments_id_is_query(comment_id: int) -> Select:
    query = get_all_query()
    query = query.join(DBComment).filter(DBComment.id.__eq__(comment_id))
    query = query.options(joinedload(DBPost.author))
    query = query.options(selectinload(DBPost.comments))
    query = query.options(selectinload(DBPost.likes))
    return query
                

async def get_comments_id_is(comment_id: int, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaPost]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBComment).filter(DBComment.id.__eq__(comment_id))
    query = query.options(joinedload(DBPost.author))
    query = query.options(selectinload(DBPost.comments))
    query = query.options(selectinload(DBPost.likes))
    return (await db.scalars(query)).all()
                

def get_comments_is_query(comment: SchemaBaseComment) -> Select:
    query = get_all_query()
    query = query.join(DBComment).filter(DBComment.id.__eq__(comment.id))
    query = query.options(joinedload(DBPost.author))
    query = query.options(selectinload(DBPost.comments))
    query = query.options(selectinload(DBPost.likes))
    return query
                

async def get_comments_is(comment: SchemaBaseComment, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaPost]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBComment).filter(DBComment.id.__eq__(comment.id))
    query = query.options(joinedload(DBPost.author))
    query = query.options(selectinload(DBPost.comments))
    query = query.options(selectinload(DBPost.likes))
    return (await db.scalars(query)).all()
                

def get_comments_id_has_query(comment_ids: List[int]) -> Select:
    query = get_all_query()
    query = query.join(DBComment).filter(DBComment.id.in_(comment_ids))
    query = query.options(joinedload(DBPost.author))
    query = query.options(selectinload(DBPost.comments))
    query = query.options(selectinload(DBPost.likes))
    return query
                

async def get_comments_id_has(comment_ids: List[int], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaPost]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBComment).filter(DBComment.id.in_(comment_ids))
    query = query.options(joinedload(DBPost.author))
    query = query.options(selectinload(DBPost.comments))
    query = query.options(selectinload(DBPost.likes))
    return (await db.scalars(query)).all()
                

def get_comments_has_query(comments: List[SchemaBaseComment]) -> Select:
    query = get_all_query()
    query = query.join(DBComment).filter(DBComment.id.in_(map(lambda x: x.id, comments)))
    query = query.options(joinedload(DBPost.author))
    query = query.options(selectinload(DBPost.comments))
    query = query.options(selectinload(DBPost.likes))
    return query
                

async def get_comments_has(comments: List[SchemaBaseComment], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaPost]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBComment).filter(DBComment.id.in_(map(lambda x: x.id, comments)))
    query = query.options(joinedload(DBPost.author))
    query = query.options(selectinload(DBPost.comments))
    query = query.options(selectinload(DBPost.likes))
    return (await db.scalars(query)).all()
                

def get_likes_id_is_query(post_like_id: int) -> Select:
    query = get_all_query()
    query = query.join(DBPostLike).filter(DBPostLike.id.__eq__(post_like_id))
    query = query.options(joinedload(DBPost.author))
    query = query.options(selectinload(DBPost.comments))
    query = query.options(selectinload(DBPost.likes))
    return query
                

async def get_likes_id_is(post_like_id: int, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaPost]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBPostLike).filter(DBPostLike.id.__eq__(post_like_id))
    query = query.options(joinedload(DBPost.author))
    query = query.options(selectinload(DBPost.comments))
    query = query.options(selectinload(DBPost.likes))
    return (await db.scalars(query)).all()
                

def get_likes_is_query(post_like: SchemaBasePostLike) -> Select:
    query = get_all_query()
    query = query.join(DBPostLike).filter(DBPostLike.id.__eq__(post_like.id))
    query = query.options(joinedload(DBPost.author))
    query = query.options(selectinload(DBPost.comments))
    query = query.options(selectinload(DBPost.likes))
    return query
                

async def get_likes_is(post_like: SchemaBasePostLike, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaPost]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBPostLike).filter(DBPostLike.id.__eq__(post_like.id))
    query = query.options(joinedload(DBPost.author))
    query = query.options(selectinload(DBPost.comments))
    query = query.options(selectinload(DBPost.likes))
    return (await db.scalars(query)).all()
                

def get_likes_id_has_query(post_like_ids: List[int]) -> Select:
    query = get_all_query()
    query = query.join(DBPostLike).filter(DBPostLike.id.in_(post_like_ids))
    query = query.options(joinedload(DBPost.author))
    query = query.options(selectinload(DBPost.comments))
    query = query.options(selectinload(DBPost.likes))
    return query
                

async def get_likes_id_has(post_like_ids: List[int], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaPost]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBPostLike).filter(DBPostLike.id.in_(post_like_ids))
    query = query.options(joinedload(DBPost.author))
    query = query.options(selectinload(DBPost.comments))
    query = query.options(selectinload(DBPost.likes))
    return (await db.scalars(query)).all()
                

def get_likes_has_query(post_likes: List[SchemaBasePostLike]) -> Select:
    query = get_all_query()
    query = query.join(DBPostLike).filter(DBPostLike.id.in_(map(lambda x: x.id, post_likes)))
    query = query.options(joinedload(DBPost.author))
    query = query.options(selectinload(DBPost.comments))
    query = query.options(selectinload(DBPost.likes))
    return query
                

async def get_likes_has(post_likes: List[SchemaBasePostLike], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaPost]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBPostLike).filter(DBPostLike.id.in_(map(lambda x: x.id, post_likes)))
    query = query.options(joinedload(DBPost.author))
    query = query.options(selectinload(DBPost.comments))
    query = query.options(selectinload(DBPost.likes))
    return (await db.scalars(query)).all()
                
