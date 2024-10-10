# generate_hash: fdf7475ad75fb5bca5663bb01c4b73d1
"""
This file was automatically generated in 2024-10-10 15:49:18.794297
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
from ..schemas import *

NOT_FOUND = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item Not found")


# ------------------------Query Routes------------------------
def get_one(user_ident: int, db=Depends(get_db)) -> DBUser:
    res = db.get(DBUser, user_ident)
    if res and res.deleted_at is None:
        return res
    raise NOT_FOUND


def batch_get(user_idents: List[int], db=Depends(get_db)) -> Page[SchemaBaseUser]:
    query = select(DBUser).filter(DBUser.deleted_at.is_(None)).filter(DBUser.id.in_(user_idents))
    return paginate(db, query)

class QueryParams(BaseModel):
    class SortParams(BaseModel):
        class StorFieldEnum(str, Enum):
            user_key = "user_key"
            sex = "sex"
            title = "title"
            name = "name"
            desc = "desc"
            bg_img = "bg_img"
            hot_level = "hot_level"
            star_level = "star_level"
            avatar = "avatar"

        field: StorFieldEnum
        is_desc: bool = False

    user_key: Optional[str] = None
    user_key_like: Optional[str] = None
    sex: Optional[bool] = None
    title: Optional[str] = None
    title_like: Optional[str] = None
    name: Optional[str] = None
    name_like: Optional[str] = None
    desc: Optional[str] = None
    desc_like: Optional[str] = None
    bg_img: Optional[str] = None
    bg_img_like: Optional[str] = None
    hot_level: Optional[int] = None
    star_level: Optional[int] = None
    avatar: Optional[Optional[str]] = None
    sort_by: List[SortParams] = Field(default_factory=list)

def get_all_query(params: QueryParams = Body()) -> Select:
    query = select(DBUser).filter(DBUser.deleted_at.is_(None))
    if params.user_key is not None:
        query = query.filter(DBUser.user_key.__eq__(params.user_key))
    if params.user_key_like is not None:
        query = query.filter(DBUser.user_key.like(params.user_key_like))
    if params.sex is not None:
        query = query.filter(DBUser.sex.__eq__(params.sex))
    if params.title is not None:
        query = query.filter(DBUser.title.__eq__(params.title))
    if params.title_like is not None:
        query = query.filter(DBUser.title.like(params.title_like))
    if params.name is not None:
        query = query.filter(DBUser.name.__eq__(params.name))
    if params.name_like is not None:
        query = query.filter(DBUser.name.like(params.name_like))
    if params.desc is not None:
        query = query.filter(DBUser.desc.__eq__(params.desc))
    if params.desc_like is not None:
        query = query.filter(DBUser.desc.like(params.desc_like))
    if params.bg_img is not None:
        query = query.filter(DBUser.bg_img.__eq__(params.bg_img))
    if params.bg_img_like is not None:
        query = query.filter(DBUser.bg_img.like(params.bg_img_like))
    if params.hot_level is not None:
        query = query.filter(DBUser.hot_level.__eq__(params.hot_level))
    if params.star_level is not None:
        query = query.filter(DBUser.star_level.__eq__(params.star_level))
    if params.avatar is not None:
        query = query.filter(DBUser.avatar.__eq__(params.avatar))
    for sort_item in params.sort_by:
        if sort_item.is_desc:
            query = query.order_by(getattr(DBUser, sort_item.field).desc())
        else:
            query = query.order_by(getattr(DBUser, sort_item.field))
    return query


def get_all(
        query=Depends(get_all_query),
        db=Depends(get_db),
) -> Page[SchemaBaseUser]:
    return paginate(db, query)


def get_link_all(
        query=Depends(get_all_query),
        db=Depends(get_db)
) -> Page[SchemaUser]:
    return paginate(db, query)
# ---------------------User Query Routes----------------------


# -----------------------Create Routes------------------------
def create_one_model(model: SchemaBaseUser, db=Depends(get_db)) -> DBUser:
    user = DBUser(**model.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_one(
        user_key: str,
        sex: bool,
        title: str,
        name: str,
        desc: str,
        bg_img: str,
        hot_level: int,
        star_level: int,
        avatar: Optional[str] = None,
        db=Depends(get_db)
) -> DBUser:
    user = SchemaBaseUser(
        user_key=user_key,
        sex=sex,
        title=title,
        name=name,
        desc=desc,
        bg_img=bg_img,
        hot_level=hot_level,
        star_level=star_level,
        avatar=avatar,
    )
    return create_one_model(user, db)


# -----------------------Update Routes------------------------
def update_one(
        user_ident: int,
        user_key: Optional[str] = None,
        sex: Optional[bool] = None,
        title: Optional[str] = None,
        name: Optional[str] = None,
        desc: Optional[str] = None,
        bg_img: Optional[str] = None,
        hot_level: Optional[int] = None,
        star_level: Optional[int] = None,
        avatar: Optional[Optional[str]] = None,
        db=Depends(get_db)) -> DBUser:
    res = db.get(DBUser, user_ident)
    if not res or res.deleted_at is not None:
        raise NOT_FOUND
    if user_key is not None:
        res.user_key = user_key
    if sex is not None:
        res.sex = sex
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
    if avatar is not None:
        res.avatar = avatar
    res.updated_at = datetime.datetime.now()
    db.commit()
    db.refresh(res)
    return SchemaBaseUser.model_validate(res)


# -----------------------Delete Routes------------------------
def delete_one(user_ident: int, db=Depends(get_db)):
    res = db.get(DBUser, user_ident)
    if not res or res.deleted_at is not None:
        raise NOT_FOUND
# TODO
    res.deleted_at = datetime.datetime.now()
    db.commit()
    return {'message': 'Deleted', 'id': user_ident}


# ----------------------Relation Routes-----------------------


def get_info_blocks_id_is_query(info_block_id: int, query=Depends(get_all_query)) -> Select:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBInfoBlock).filter(DBInfoBlock.id.__eq__(info_block_id))
    query = query.options(selectinload(DBUser.info_blocks))
    query = query.options(selectinload(DBUser.certified_records))
    return query
                

def get_info_blocks_id_is(info_block_id: int, db=Depends(get_db), query=Depends(get_all_query)) -> List[DBUser]:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBInfoBlock).filter(DBInfoBlock.id.__eq__(info_block_id))
    query = query.options(selectinload(DBUser.info_blocks))
    query = query.options(selectinload(DBUser.certified_records))
    return db.scalars(query).all()
                

def get_info_blocks_is_query(info_block: SchemaBaseInfoBlock, query=Depends(get_all_query)) -> Select:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBInfoBlock).filter(DBInfoBlock.id.__eq__(info_block.id))
    query = query.options(selectinload(DBUser.info_blocks))
    query = query.options(selectinload(DBUser.certified_records))
    return query
                

def get_info_blocks_is(info_block: SchemaBaseInfoBlock, db=Depends(get_db), query=Depends(get_all_query)) -> List[DBUser]:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBInfoBlock).filter(DBInfoBlock.id.__eq__(info_block.id))
    query = query.options(selectinload(DBUser.info_blocks))
    query = query.options(selectinload(DBUser.certified_records))
    return db.scalars(query).all()
                

def get_info_blocks_id_has_query(info_block_ids: List[int], query=Depends(get_all_query)) -> Select:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBInfoBlock).filter(DBInfoBlock.id.in_(info_block_ids))
    query = query.options(selectinload(DBUser.info_blocks))
    query = query.options(selectinload(DBUser.certified_records))
    return query
                

def get_info_blocks_id_has(info_block_ids: List[int], db=Depends(get_db), query=Depends(get_all_query)) -> List[DBUser]:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBInfoBlock).filter(DBInfoBlock.id.in_(info_block_ids))
    query = query.options(selectinload(DBUser.info_blocks))
    query = query.options(selectinload(DBUser.certified_records))
    return db.scalars(query).all()
                

def get_info_blocks_has_query(info_blocks: List[SchemaBaseInfoBlock], query=Depends(get_all_query)) -> Select:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBInfoBlock).filter(DBInfoBlock.id.in_(map(lambda x: x.id, info_blocks)))
    query = query.options(selectinload(DBUser.info_blocks))
    query = query.options(selectinload(DBUser.certified_records))
    return query
                

def get_info_blocks_has(info_blocks: List[SchemaBaseInfoBlock], db=Depends(get_db), query=Depends(get_all_query)) -> List[DBUser]:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBInfoBlock).filter(DBInfoBlock.id.in_(map(lambda x: x.id, info_blocks)))
    query = query.options(selectinload(DBUser.info_blocks))
    query = query.options(selectinload(DBUser.certified_records))
    return db.scalars(query).all()
                

def get_certified_records_id_is_query(certified_record_id: int, query=Depends(get_all_query)) -> Select:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBCertifiedRecord).filter(DBCertifiedRecord.id.__eq__(certified_record_id))
    query = query.options(selectinload(DBUser.info_blocks))
    query = query.options(selectinload(DBUser.certified_records))
    return query
                

def get_certified_records_id_is(certified_record_id: int, db=Depends(get_db), query=Depends(get_all_query)) -> List[DBUser]:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBCertifiedRecord).filter(DBCertifiedRecord.id.__eq__(certified_record_id))
    query = query.options(selectinload(DBUser.info_blocks))
    query = query.options(selectinload(DBUser.certified_records))
    return db.scalars(query).all()
                

def get_certified_records_is_query(certified_record: SchemaBaseCertifiedRecord, query=Depends(get_all_query)) -> Select:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBCertifiedRecord).filter(DBCertifiedRecord.id.__eq__(certified_record.id))
    query = query.options(selectinload(DBUser.info_blocks))
    query = query.options(selectinload(DBUser.certified_records))
    return query
                

def get_certified_records_is(certified_record: SchemaBaseCertifiedRecord, db=Depends(get_db), query=Depends(get_all_query)) -> List[DBUser]:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBCertifiedRecord).filter(DBCertifiedRecord.id.__eq__(certified_record.id))
    query = query.options(selectinload(DBUser.info_blocks))
    query = query.options(selectinload(DBUser.certified_records))
    return db.scalars(query).all()
                

def get_certified_records_id_has_query(certified_record_ids: List[int], query=Depends(get_all_query)) -> Select:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBCertifiedRecord).filter(DBCertifiedRecord.id.in_(certified_record_ids))
    query = query.options(selectinload(DBUser.info_blocks))
    query = query.options(selectinload(DBUser.certified_records))
    return query
                

def get_certified_records_id_has(certified_record_ids: List[int], db=Depends(get_db), query=Depends(get_all_query)) -> List[DBUser]:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBCertifiedRecord).filter(DBCertifiedRecord.id.in_(certified_record_ids))
    query = query.options(selectinload(DBUser.info_blocks))
    query = query.options(selectinload(DBUser.certified_records))
    return db.scalars(query).all()
                

def get_certified_records_has_query(certified_records: List[SchemaBaseCertifiedRecord], query=Depends(get_all_query)) -> Select:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBCertifiedRecord).filter(DBCertifiedRecord.id.in_(map(lambda x: x.id, certified_records)))
    query = query.options(selectinload(DBUser.info_blocks))
    query = query.options(selectinload(DBUser.certified_records))
    return query
                

def get_certified_records_has(certified_records: List[SchemaBaseCertifiedRecord], db=Depends(get_db), query=Depends(get_all_query)) -> List[DBUser]:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBCertifiedRecord).filter(DBCertifiedRecord.id.in_(map(lambda x: x.id, certified_records)))
    query = query.options(selectinload(DBUser.info_blocks))
    query = query.options(selectinload(DBUser.certified_records))
    return db.scalars(query).all()
                
