# generate_hash: d267269d595bc74a02a37f40caceaf31
"""
This file was automatically generated in 2024-09-03 17:14:12.334457
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
async def get_one(info_block_ident: int, db=Depends(get_db)) -> SchemaBaseInfoBlock:
    res = await db.get(DBInfoBlock, info_block_ident)
    if res and res.deleted_at is None:
        return res
    raise NOT_FOUND


async def batch_get(info_block_idents: List[int], db=Depends(get_db)) -> Page[SchemaBaseInfoBlock]:
    query = select(DBInfoBlock).filter(DBInfoBlock.deleted_at.is_(None)).filter(DBInfoBlock.id.in_(info_block_idents))
    return await paginate(db, query)


def get_all_query(
        filter_type: Optional[str] = None,
        filter_title: Optional[str] = None,
        filter_sub_title: Optional[str] = None,
        filter_desc: Optional[str] = None,
        filter_tags: Optional[str] = None,
        filter_show: Optional[bool] = None,
        filter_time_start: Optional[datetime.date] = None,
        filter_time_end: Optional[datetime.date] = None,
        sort_by: Optional[str] = None, is_desc: bool = False,
) -> Select:
    query = select(DBInfoBlock).filter(DBInfoBlock.deleted_at.is_(None))
    if filter_type is not None:
        query = query.filter(DBInfoBlock.type.__eq__(filter_type))
    if filter_title is not None:
        query = query.filter(DBInfoBlock.title.__eq__(filter_title))
    if filter_sub_title is not None:
        query = query.filter(DBInfoBlock.sub_title.__eq__(filter_sub_title))
    if filter_desc is not None:
        query = query.filter(DBInfoBlock.desc.__eq__(filter_desc))
    if filter_tags is not None:
        query = query.filter(DBInfoBlock.tags.__eq__(filter_tags))
    if filter_show is not None:
        query = query.filter(DBInfoBlock.show.__eq__(filter_show))
    if filter_time_start is not None:
        query = query.filter(DBInfoBlock.time_start.__eq__(filter_time_start))
    if filter_time_end is not None:
        query = query.filter(DBInfoBlock.time_end.__eq__(filter_time_end))
    if sort_by is not None:
        if is_desc:
            query = query.order_by(getattr(DBInfoBlock, sort_by).desc())
        else:
            query = query.order_by(getattr(DBInfoBlock, sort_by))
    return query


async def get_all(
        paginate_parmas: Params,
        query=Depends(get_all_query),
        db=Depends(get_db),
) -> Page[SchemaBaseInfoBlock]:
    return await paginate(db, query, params=paginate_parmas)


async def get_link_all(
        paginate_parmas: Params,
        query=Depends(get_all_query),
        db=Depends(get_db)
) -> Page[SchemaInfoBlock]:
    return await paginate(db, query, params=paginate_parmas)
# ---------------------User Query Routes----------------------


# -----------------------Create Routes------------------------
async def create_one(
        type: str,
        title: str,
        sub_title: str,
        desc: str,
        tags: str,
        show: bool,
        time_start: datetime.date,
        time_end: datetime.date,
        db=Depends(get_db)
) -> SchemaBaseInfoBlock:
    info_block = SchemaBaseInfoBlock(
        type=type,
        title=title,
        sub_title=sub_title,
        desc=desc,
        tags=tags,
        show=show,
        time_start=time_start,
        time_end=time_end,
    )
    info_block = DBInfoBlock(**info_block.model_dump())
    db.add(info_block)
    await db.commit()
    await db.refresh(info_block)
    return SchemaBaseInfoBlock.model_validate(info_block)


# -----------------------Update Routes------------------------
async def update_one(
        info_block_ident: int,
        type: Optional[str] = None,
        title: Optional[str] = None,
        sub_title: Optional[str] = None,
        desc: Optional[str] = None,
        tags: Optional[str] = None,
        show: Optional[bool] = None,
        time_start: Optional[datetime.date] = None,
        time_end: Optional[datetime.date] = None,
        db=Depends(get_db)) -> SchemaBaseInfoBlock:
    res = await db.get(DBInfoBlock, info_block_ident)
    if not res or res.deleted_at is not None:
        raise NOT_FOUND
    if type is not None:
        res.type = type
    if title is not None:
        res.title = title
    if sub_title is not None:
        res.sub_title = sub_title
    if desc is not None:
        res.desc = desc
    if tags is not None:
        res.tags = tags
    if show is not None:
        res.show = show
    if time_start is not None:
        res.time_start = time_start
    if time_end is not None:
        res.time_end = time_end
    res.updated_at = datetime.datetime.now()
    await db.commit()
    await db.refresh(res)
    return SchemaBaseInfoBlock.model_validate(res)


# -----------------------Delete Routes------------------------
async def delete_one(info_block_ident: int, db=Depends(get_db)):
    res = await db.get(DBInfoBlock, info_block_ident)
    if not res or res.deleted_at is not None:
        raise NOT_FOUND
# TODO
    res.deleted_at = datetime.datetime.now()
    await db.commit()
    return {'message': 'Deleted', 'id': info_block_ident}


# ----------------------Relation Routes-----------------------


def get_user_id_is_query(user_id: int) -> Select:
    query = get_all_query()
    query = query.join(DBUser).filter(DBUser.id.__eq__(user_id))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return query
                

async def get_user_id_is(user_id: int, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaInfoBlock]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBUser).filter(DBUser.id.__eq__(user_id))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return (await db.scalars(query)).all()
                

def get_user_is_query(user: SchemaBaseUser) -> Select:
    query = get_all_query()
    query = query.join(DBUser).filter(DBUser.id.__eq__(user.id))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return query
                

async def get_user_is(user: SchemaBaseUser, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaInfoBlock]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBUser).filter(DBUser.id.__eq__(user.id))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return (await db.scalars(query)).all()
                

def get_user_id_has_query(user_ids: List[int]) -> Select:
    query = get_all_query()
    query = query.join(DBUser).filter(DBUser.id.in_(user_ids))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return query
                

async def get_user_id_has(user_ids: List[int], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaInfoBlock]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBUser).filter(DBUser.id.in_(user_ids))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return (await db.scalars(query)).all()
                

def get_user_has_query(users: List[SchemaBaseUser]) -> Select:
    query = get_all_query()
    query = query.join(DBUser).filter(DBUser.id.in_(map(lambda x: x.id, users)))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return query
                

async def get_user_has(users: List[SchemaBaseUser], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaInfoBlock]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBUser).filter(DBUser.id.in_(map(lambda x: x.id, users)))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return (await db.scalars(query)).all()
                

def get_certified_records_id_is_query(certified_record_id: int) -> Select:
    query = get_all_query()
    query = query.join(DBCertifiedRecord).filter(DBCertifiedRecord.id.__eq__(certified_record_id))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return query
                

async def get_certified_records_id_is(certified_record_id: int, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaInfoBlock]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBCertifiedRecord).filter(DBCertifiedRecord.id.__eq__(certified_record_id))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return (await db.scalars(query)).all()
                

def get_certified_records_is_query(certified_record: SchemaBaseCertifiedRecord) -> Select:
    query = get_all_query()
    query = query.join(DBCertifiedRecord).filter(DBCertifiedRecord.id.__eq__(certified_record.id))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return query
                

async def get_certified_records_is(certified_record: SchemaBaseCertifiedRecord, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaInfoBlock]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBCertifiedRecord).filter(DBCertifiedRecord.id.__eq__(certified_record.id))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return (await db.scalars(query)).all()
                

def get_certified_records_id_has_query(certified_record_ids: List[int]) -> Select:
    query = get_all_query()
    query = query.join(DBCertifiedRecord).filter(DBCertifiedRecord.id.in_(certified_record_ids))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return query
                

async def get_certified_records_id_has(certified_record_ids: List[int], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaInfoBlock]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBCertifiedRecord).filter(DBCertifiedRecord.id.in_(certified_record_ids))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return (await db.scalars(query)).all()
                

def get_certified_records_has_query(certified_records: List[SchemaBaseCertifiedRecord]) -> Select:
    query = get_all_query()
    query = query.join(DBCertifiedRecord).filter(DBCertifiedRecord.id.in_(map(lambda x: x.id, certified_records)))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return query
                

async def get_certified_records_has(certified_records: List[SchemaBaseCertifiedRecord], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaInfoBlock]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBCertifiedRecord).filter(DBCertifiedRecord.id.in_(map(lambda x: x.id, certified_records)))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return (await db.scalars(query)).all()
                
