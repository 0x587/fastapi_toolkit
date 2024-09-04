# generate_hash: 6d7f71822c79928a3ec3869e5c51da28
"""
This file was automatically generated in 2024-09-04 16:25:51.563141
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

class QueryParams(BaseModel):
    class SortParams(BaseModel):
        class StorFieldEnum(str, Enum):
            type = "type"
            title = "title"
            sub_title = "sub_title"
            desc = "desc"
            tags = "tags"
            show = "show"
            time_start = "time_start"
            time_end = "time_end"

        field: StorFieldEnum
        is_desc: bool = False

    type: Optional[str] = None
    type_like = None
    title: Optional[str] = None
    title_like = None
    sub_title: Optional[str] = None
    sub_title_like = None
    desc: Optional[str] = None
    desc_like = None
    tags: Optional[str] = None
    tags_like = None
    show: Optional[bool] = None
    time_start: Optional[datetime.date] = None
    time_end: Optional[datetime.date] = None
    sort_by: List[SortParams] = Field(default_factory=list)

def get_all_query(params: QueryParams = Body()) -> Select:
    query = select(DBInfoBlock).filter(DBInfoBlock.deleted_at.is_(None))
    if params.type is not None:
        query = query.filter(DBInfoBlock.type.__eq__(params.type))
    if params.type_like is not None:
        query = query.filter(DBInfoBlock.type.like(params.type_like))
    if params.title is not None:
        query = query.filter(DBInfoBlock.title.__eq__(params.title))
    if params.title_like is not None:
        query = query.filter(DBInfoBlock.title.like(params.title_like))
    if params.sub_title is not None:
        query = query.filter(DBInfoBlock.sub_title.__eq__(params.sub_title))
    if params.sub_title_like is not None:
        query = query.filter(DBInfoBlock.sub_title.like(params.sub_title_like))
    if params.desc is not None:
        query = query.filter(DBInfoBlock.desc.__eq__(params.desc))
    if params.desc_like is not None:
        query = query.filter(DBInfoBlock.desc.like(params.desc_like))
    if params.tags is not None:
        query = query.filter(DBInfoBlock.tags.__eq__(params.tags))
    if params.tags_like is not None:
        query = query.filter(DBInfoBlock.tags.like(params.tags_like))
    if params.show is not None:
        query = query.filter(DBInfoBlock.show.__eq__(params.show))
    if params.time_start is not None:
        query = query.filter(DBInfoBlock.time_start.__eq__(params.time_start))
    if params.time_end is not None:
        query = query.filter(DBInfoBlock.time_end.__eq__(params.time_end))
    for sort_item in params.sort_by:
        if sort_item.is_desc:
            query = query.order_by(getattr(DBInfoBlock, sort_item.field).desc())
        else:
            query = query.order_by(getattr(DBInfoBlock, sort_item.field))
    return query


async def get_all(
        query=Depends(get_all_query),
        db=Depends(get_db),
) -> Page[SchemaBaseInfoBlock]:
    return await paginate(db, query)


async def get_link_all(
        query=Depends(get_all_query),
        db=Depends(get_db)
) -> Page[SchemaInfoBlock]:
    return await paginate(db, query)
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


def get_user_id_is_query(self, user_id: int) -> Select:
    query = self.get_all_query()
    query = query.join(DBUser).filter(DBUser.id.__eq__(user_id))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return query
                

async def get_user_id_is(self, user_id: int, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaInfoBlock]:
    if type(query) is not Select:
        query = self.get_all_query()
    query = query.join(DBUser).filter(DBUser.id.__eq__(user_id))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return (await db.scalars(query)).all()
                

def get_user_is_query(self, user: SchemaBaseUser) -> Select:
    query = self.get_all_query()
    query = query.join(DBUser).filter(DBUser.id.__eq__(user.id))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return query
                

async def get_user_is(self, user: SchemaBaseUser, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaInfoBlock]:
    if type(query) is not Select:
        query = self.get_all_query()
    query = query.join(DBUser).filter(DBUser.id.__eq__(user.id))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return (await db.scalars(query)).all()
                

def get_user_id_has_query(self, user_ids: List[int]) -> Select:
    query = self.get_all_query()
    query = query.join(DBUser).filter(DBUser.id.in_(user_ids))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return query
                

async def get_user_id_has(self, user_ids: List[int], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaInfoBlock]:
    if type(query) is not Select:
        query = self.get_all_query()
    query = query.join(DBUser).filter(DBUser.id.in_(user_ids))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return (await db.scalars(query)).all()
                

def get_user_has_query(self, users: List[SchemaBaseUser]) -> Select:
    query = self.get_all_query()
    query = query.join(DBUser).filter(DBUser.id.in_(map(lambda x: x.id, users)))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return query
                

async def get_user_has(self, users: List[SchemaBaseUser], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaInfoBlock]:
    if type(query) is not Select:
        query = self.get_all_query()
    query = query.join(DBUser).filter(DBUser.id.in_(map(lambda x: x.id, users)))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return (await db.scalars(query)).all()
                

def get_certified_records_id_is_query(self, certified_record_id: int) -> Select:
    query = self.get_all_query()
    query = query.join(DBCertifiedRecord).filter(DBCertifiedRecord.id.__eq__(certified_record_id))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return query
                

async def get_certified_records_id_is(self, certified_record_id: int, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaInfoBlock]:
    if type(query) is not Select:
        query = self.get_all_query()
    query = query.join(DBCertifiedRecord).filter(DBCertifiedRecord.id.__eq__(certified_record_id))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return (await db.scalars(query)).all()
                

def get_certified_records_is_query(self, certified_record: SchemaBaseCertifiedRecord) -> Select:
    query = self.get_all_query()
    query = query.join(DBCertifiedRecord).filter(DBCertifiedRecord.id.__eq__(certified_record.id))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return query
                

async def get_certified_records_is(self, certified_record: SchemaBaseCertifiedRecord, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaInfoBlock]:
    if type(query) is not Select:
        query = self.get_all_query()
    query = query.join(DBCertifiedRecord).filter(DBCertifiedRecord.id.__eq__(certified_record.id))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return (await db.scalars(query)).all()
                

def get_certified_records_id_has_query(self, certified_record_ids: List[int]) -> Select:
    query = self.get_all_query()
    query = query.join(DBCertifiedRecord).filter(DBCertifiedRecord.id.in_(certified_record_ids))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return query
                

async def get_certified_records_id_has(self, certified_record_ids: List[int], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaInfoBlock]:
    if type(query) is not Select:
        query = self.get_all_query()
    query = query.join(DBCertifiedRecord).filter(DBCertifiedRecord.id.in_(certified_record_ids))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return (await db.scalars(query)).all()
                

def get_certified_records_has_query(self, certified_records: List[SchemaBaseCertifiedRecord]) -> Select:
    query = self.get_all_query()
    query = query.join(DBCertifiedRecord).filter(DBCertifiedRecord.id.in_(map(lambda x: x.id, certified_records)))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return query
                

async def get_certified_records_has(self, certified_records: List[SchemaBaseCertifiedRecord], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaInfoBlock]:
    if type(query) is not Select:
        query = self.get_all_query()
    query = query.join(DBCertifiedRecord).filter(DBCertifiedRecord.id.in_(map(lambda x: x.id, certified_records)))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return (await db.scalars(query)).all()
                
