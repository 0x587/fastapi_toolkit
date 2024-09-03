# generate_hash: 86cd883088769b9faf575cc441244af7
"""
This file was automatically generated in 2024-09-03 17:14:12.330902
"""

from typing import List, Optional
from fastapi import Depends, Response, HTTPException, status
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
import datetime
from sqlalchemy import select, Select
from sqlalchemy.orm import joinedload, selectinload
from ..db import get_db
from ..models import *
from ..schemas import *

NOT_FOUND = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item Not found")


# ------------------------Query Routes------------------------
async def get_one(user_ident: int, db=Depends(get_db)) -> SchemaBaseUser:
    res = await db.get(DBUser, user_ident)
    if res and res.deleted_at is None:
        return res
    raise NOT_FOUND


async def batch_get(user_idents: List[int], db=Depends(get_db)) -> Page[SchemaBaseUser]:
    query = select(DBUser).filter(DBUser.deleted_at.is_(None)).filter(DBUser.id.in_(user_idents))
    return await paginate(db, query)


def get_all_query(
        filter_sex: Optional[bool] = None,
        filter_title: Optional[str] = None,
        filter_name: Optional[str] = None,
        filter_desc: Optional[str] = None,
        filter_avatar: Optional[str] = None,
        filter_bg_img: Optional[str] = None,
        filter_hot_level: Optional[int] = None,
        filter_star_level: Optional[int] = None,
        filter_user_key: Optional[str] = None,
        sort_by: Optional[str] = None, is_desc: bool = False,
) -> Select:
    query = select(DBUser).filter(DBUser.deleted_at.is_(None))
    if filter_sex is not None:
        query = query.filter(DBUser.sex.__eq__(filter_sex))
    if filter_title is not None:
        query = query.filter(DBUser.title.__eq__(filter_title))
    if filter_name is not None:
        query = query.filter(DBUser.name.__eq__(filter_name))
    if filter_desc is not None:
        query = query.filter(DBUser.desc.__eq__(filter_desc))
    if filter_avatar is not None:
        query = query.filter(DBUser.avatar.__eq__(filter_avatar))
    if filter_bg_img is not None:
        query = query.filter(DBUser.bg_img.__eq__(filter_bg_img))
    if filter_hot_level is not None:
        query = query.filter(DBUser.hot_level.__eq__(filter_hot_level))
    if filter_star_level is not None:
        query = query.filter(DBUser.star_level.__eq__(filter_star_level))
    if filter_user_key is not None:
        query = query.filter(DBUser.user_key.__eq__(filter_user_key))
    if sort_by is not None:
        if is_desc:
            query = query.order_by(getattr(DBUser, sort_by).desc())
        else:
            query = query.order_by(getattr(DBUser, sort_by))
    return query


async def get_all(
        paginate_parmas: Params,
        query=Depends(get_all_query),
        db=Depends(get_db),
) -> Page[SchemaBaseUser]:
    return await paginate(db, query, params=paginate_parmas)


async def get_link_all(
        paginate_parmas: Params,
        query=Depends(get_all_query),
        db=Depends(get_db)
) -> Page[SchemaUser]:
    return await paginate(db, query, params=paginate_parmas)
# ---------------------User Query Routes----------------------


# -----------------------Create Routes------------------------
async def create_one(
        sex: bool,
        title: str,
        name: str,
        desc: str,
        avatar: str,
        bg_img: str,
        hot_level: int,
        star_level: int,
        user_key: str,
        db=Depends(get_db)
) -> SchemaBaseUser:
    user = SchemaBaseUser(
        sex=sex,
        title=title,
        name=name,
        desc=desc,
        avatar=avatar,
        bg_img=bg_img,
        hot_level=hot_level,
        star_level=star_level,
        user_key=user_key,
    )
    user = DBUser(**user.model_dump())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return SchemaBaseUser.model_validate(user)


# -----------------------Update Routes------------------------
async def update_one(
        user_ident: int,
        sex: Optional[bool] = None,
        title: Optional[str] = None,
        name: Optional[str] = None,
        desc: Optional[str] = None,
        avatar: Optional[str] = None,
        bg_img: Optional[str] = None,
        hot_level: Optional[int] = None,
        star_level: Optional[int] = None,
        user_key: Optional[str] = None,
        db=Depends(get_db)) -> SchemaBaseUser:
    res = await db.get(DBUser, user_ident)
    if not res or res.deleted_at is not None:
        raise NOT_FOUND
    if sex is not None:
        res.sex = sex
    if title is not None:
        res.title = title
    if name is not None:
        res.name = name
    if desc is not None:
        res.desc = desc
    if avatar is not None:
        res.avatar = avatar
    if bg_img is not None:
        res.bg_img = bg_img
    if hot_level is not None:
        res.hot_level = hot_level
    if star_level is not None:
        res.star_level = star_level
    if user_key is not None:
        res.user_key = user_key
    res.updated_at = datetime.datetime.now()
    await db.commit()
    await db.refresh(res)
    return SchemaBaseUser.model_validate(res)


# -----------------------Delete Routes------------------------
async def delete_one(user_ident: int, db=Depends(get_db)):
    res = await db.get(DBUser, user_ident)
    if not res or res.deleted_at is not None:
        raise NOT_FOUND
# TODO
    res.deleted_at = datetime.datetime.now()
    await db.commit()
    return {'message': 'Deleted', 'id': user_ident}


# ----------------------Relation Routes-----------------------


def get_info_blocks_id_is_query(info_block_id: int) -> Select:
    query = get_all_query()
    query = query.join(DBInfoBlock).filter(DBInfoBlock.id.__eq__(info_block_id))
    query = query.options(selectinload(DBUser.info_blocks))
    query = query.options(selectinload(DBUser.certified_records))
    return query
                

async def get_info_blocks_id_is(info_block_id: int, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaUser]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBInfoBlock).filter(DBInfoBlock.id.__eq__(info_block_id))
    query = query.options(selectinload(DBUser.info_blocks))
    query = query.options(selectinload(DBUser.certified_records))
    return (await db.scalars(query)).all()
                

def get_info_blocks_is_query(info_block: SchemaBaseInfoBlock) -> Select:
    query = get_all_query()
    query = query.join(DBInfoBlock).filter(DBInfoBlock.id.__eq__(info_block.id))
    query = query.options(selectinload(DBUser.info_blocks))
    query = query.options(selectinload(DBUser.certified_records))
    return query
                

async def get_info_blocks_is(info_block: SchemaBaseInfoBlock, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaUser]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBInfoBlock).filter(DBInfoBlock.id.__eq__(info_block.id))
    query = query.options(selectinload(DBUser.info_blocks))
    query = query.options(selectinload(DBUser.certified_records))
    return (await db.scalars(query)).all()
                

def get_info_blocks_id_has_query(info_block_ids: List[int]) -> Select:
    query = get_all_query()
    query = query.join(DBInfoBlock).filter(DBInfoBlock.id.in_(info_block_ids))
    query = query.options(selectinload(DBUser.info_blocks))
    query = query.options(selectinload(DBUser.certified_records))
    return query
                

async def get_info_blocks_id_has(info_block_ids: List[int], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaUser]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBInfoBlock).filter(DBInfoBlock.id.in_(info_block_ids))
    query = query.options(selectinload(DBUser.info_blocks))
    query = query.options(selectinload(DBUser.certified_records))
    return (await db.scalars(query)).all()
                

def get_info_blocks_has_query(info_blocks: List[SchemaBaseInfoBlock]) -> Select:
    query = get_all_query()
    query = query.join(DBInfoBlock).filter(DBInfoBlock.id.in_(map(lambda x: x.id, info_blocks)))
    query = query.options(selectinload(DBUser.info_blocks))
    query = query.options(selectinload(DBUser.certified_records))
    return query
                

async def get_info_blocks_has(info_blocks: List[SchemaBaseInfoBlock], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaUser]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBInfoBlock).filter(DBInfoBlock.id.in_(map(lambda x: x.id, info_blocks)))
    query = query.options(selectinload(DBUser.info_blocks))
    query = query.options(selectinload(DBUser.certified_records))
    return (await db.scalars(query)).all()
                

def get_certified_records_id_is_query(certified_record_id: int) -> Select:
    query = get_all_query()
    query = query.join(DBCertifiedRecord).filter(DBCertifiedRecord.id.__eq__(certified_record_id))
    query = query.options(selectinload(DBUser.info_blocks))
    query = query.options(selectinload(DBUser.certified_records))
    return query
                

async def get_certified_records_id_is(certified_record_id: int, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaUser]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBCertifiedRecord).filter(DBCertifiedRecord.id.__eq__(certified_record_id))
    query = query.options(selectinload(DBUser.info_blocks))
    query = query.options(selectinload(DBUser.certified_records))
    return (await db.scalars(query)).all()
                

def get_certified_records_is_query(certified_record: SchemaBaseCertifiedRecord) -> Select:
    query = get_all_query()
    query = query.join(DBCertifiedRecord).filter(DBCertifiedRecord.id.__eq__(certified_record.id))
    query = query.options(selectinload(DBUser.info_blocks))
    query = query.options(selectinload(DBUser.certified_records))
    return query
                

async def get_certified_records_is(certified_record: SchemaBaseCertifiedRecord, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaUser]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBCertifiedRecord).filter(DBCertifiedRecord.id.__eq__(certified_record.id))
    query = query.options(selectinload(DBUser.info_blocks))
    query = query.options(selectinload(DBUser.certified_records))
    return (await db.scalars(query)).all()
                

def get_certified_records_id_has_query(certified_record_ids: List[int]) -> Select:
    query = get_all_query()
    query = query.join(DBCertifiedRecord).filter(DBCertifiedRecord.id.in_(certified_record_ids))
    query = query.options(selectinload(DBUser.info_blocks))
    query = query.options(selectinload(DBUser.certified_records))
    return query
                

async def get_certified_records_id_has(certified_record_ids: List[int], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaUser]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBCertifiedRecord).filter(DBCertifiedRecord.id.in_(certified_record_ids))
    query = query.options(selectinload(DBUser.info_blocks))
    query = query.options(selectinload(DBUser.certified_records))
    return (await db.scalars(query)).all()
                

def get_certified_records_has_query(certified_records: List[SchemaBaseCertifiedRecord]) -> Select:
    query = get_all_query()
    query = query.join(DBCertifiedRecord).filter(DBCertifiedRecord.id.in_(map(lambda x: x.id, certified_records)))
    query = query.options(selectinload(DBUser.info_blocks))
    query = query.options(selectinload(DBUser.certified_records))
    return query
                

async def get_certified_records_has(certified_records: List[SchemaBaseCertifiedRecord], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaUser]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBCertifiedRecord).filter(DBCertifiedRecord.id.in_(map(lambda x: x.id, certified_records)))
    query = query.options(selectinload(DBUser.info_blocks))
    query = query.options(selectinload(DBUser.certified_records))
    return (await db.scalars(query)).all()
                
