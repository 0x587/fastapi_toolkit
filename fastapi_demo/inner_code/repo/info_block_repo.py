# generate_hash: 32e49af82abd3c99039b007a5954493a
"""
This file was automatically generated in 2024-10-13 17:00:25.474261
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
def get_one(info_block_ident: int, db=Depends(get_db)) -> DBInfoBlock:
    res = db.get(DBInfoBlock, info_block_ident)
    if res and res.deleted_at is None:
        return res
    raise NOT_FOUND


def batch_get(info_block_idents: List[int], db=Depends(get_db)) -> Page[SchemaBaseInfoBlock]:
    query = select(DBInfoBlock).filter(DBInfoBlock.deleted_at.is_(None)).filter(DBInfoBlock.id.in_(info_block_idents))
    return paginate(db, query)

class QueryParams(BaseModel):
    class SortParams(BaseModel):
        class StorFieldEnum(str, Enum):
            type = "type"
            title = "title"
            sub_title = "sub_title"
            desc = "desc"
            tags = "tags"
            time_start = "time_start"
            time_end = "time_end"
            show = "show"

        field: StorFieldEnum
        is_desc: bool = False

    type: Optional[str] = None
    type_like: Optional[str] = None
    title: Optional[str] = None
    title_like: Optional[str] = None
    sub_title: Optional[str] = None
    sub_title_like: Optional[str] = None
    desc: Optional[str] = None
    desc_like: Optional[str] = None
    tags: Optional[str] = None
    tags_like: Optional[str] = None
    time_start: Optional[datetime.date] = None
    time_end: Optional[datetime.date] = None
    show: Optional[bool] = None
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
    if params.time_start is not None:
        query = query.filter(DBInfoBlock.time_start.__eq__(params.time_start))
    if params.time_end is not None:
        query = query.filter(DBInfoBlock.time_end.__eq__(params.time_end))
    if params.show is not None:
        query = query.filter(DBInfoBlock.show.__eq__(params.show))
    for sort_item in params.sort_by:
        if sort_item.is_desc:
            query = query.order_by(getattr(DBInfoBlock, sort_item.field).desc())
        else:
            query = query.order_by(getattr(DBInfoBlock, sort_item.field))
    return query


def get_all(
        query=Depends(get_all_query),
        db=Depends(get_db),
) -> Page[SchemaBaseInfoBlock]:
    return paginate(db, query)


def get_link_all(
        query=Depends(get_all_query),
        db=Depends(get_db)
) -> Page[SchemaInfoBlock]:
    return paginate(db, query)
# ---------------------User Query Routes----------------------


# -----------------------Create Routes------------------------
def create_one_model(model: SchemaBaseInfoBlock, db=Depends(get_db)) -> DBInfoBlock:
    info_block = DBInfoBlock(**model.model_dump())
    db.add(info_block)
    db.commit()
    db.refresh(info_block)
    return info_block

def create_one(
        type: str,
        title: str,
        sub_title: str,
        desc: str,
        tags: str,
        time_start: datetime.date,
        time_end: datetime.date,
        show: bool = False,
        _fk_user_user_id: Optional[int] = None,
        db=Depends(get_db)
) -> DBInfoBlock:
    info_block = DBInfoBlock(
        type=type,
        title=title,
        sub_title=sub_title,
        desc=desc,
        tags=tags,
        time_start=time_start,
        time_end=time_end,
        show=show,
        _fk_user_user_id=_fk_user_user_id,
    )
    db.add(info_block)
    db.commit()
    db.refresh(info_block)
    return info_block


# -----------------------Update Routes------------------------
class ForceUpdate(BaseModel):
    type: Optional[bool] = Field(default=False)
    title: Optional[bool] = Field(default=False)
    sub_title: Optional[bool] = Field(default=False)
    desc: Optional[bool] = Field(default=False)
    tags: Optional[bool] = Field(default=False)
    time_start: Optional[bool] = Field(default=False)
    time_end: Optional[bool] = Field(default=False)
    show: Optional[bool] = Field(default=False)

def update_one(
        info_block_ident: int,
        type: Optional[str] = None,
        title: Optional[str] = None,
        sub_title: Optional[str] = None,
        desc: Optional[str] = None,
        tags: Optional[str] = None,
        time_start: Optional[datetime.date] = None,
        time_end: Optional[datetime.date] = None,
        show: Optional[bool] = None,
        force_update: Optional[ForceUpdate] = ForceUpdate(),
        db=Depends(get_db)) -> DBInfoBlock:
    res = db.get(DBInfoBlock, info_block_ident)
    if not res or res.deleted_at is not None:
        raise NOT_FOUND
    if type is not None or force_update.type:
        res.type = type
    if title is not None or force_update.title:
        res.title = title
    if sub_title is not None or force_update.sub_title:
        res.sub_title = sub_title
    if desc is not None or force_update.desc:
        res.desc = desc
    if tags is not None or force_update.tags:
        res.tags = tags
    if time_start is not None or force_update.time_start:
        res.time_start = time_start
    if time_end is not None or force_update.time_end:
        res.time_end = time_end
    if show is not None or force_update.show:
        res.show = show
    res.updated_at = datetime.datetime.now()
    db.commit()
    db.refresh(res)
    return SchemaBaseInfoBlock.model_validate(res)


# -----------------------Delete Routes------------------------
def delete_one(info_block_ident: int, db=Depends(get_db)):
    res = db.get(DBInfoBlock, info_block_ident)
    if not res or res.deleted_at is not None:
        raise NOT_FOUND
# TODO
    res.deleted_at = datetime.datetime.now()
    db.commit()
    return {'message': 'Deleted', 'id': info_block_ident}


# ----------------------Relation Routes-----------------------


def get_user_id_is_query(user_id: int, query=Depends(get_all_query)) -> Select:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBUser).filter(DBUser.id.__eq__(user_id))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return query
                

def get_user_id_is(user_id: int, db=Depends(get_db), query=Depends(get_all_query)) -> List[DBInfoBlock]:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBUser).filter(DBUser.id.__eq__(user_id))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return db.scalars(query).all()
                

def get_user_is_query(user: SchemaBaseUser, query=Depends(get_all_query)) -> Select:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBUser).filter(DBUser.id.__eq__(user.id))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return query
                

def get_user_is(user: SchemaBaseUser, db=Depends(get_db), query=Depends(get_all_query)) -> List[DBInfoBlock]:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBUser).filter(DBUser.id.__eq__(user.id))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return db.scalars(query).all()
                

def get_user_id_has_query(user_ids: List[int], query=Depends(get_all_query)) -> Select:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBUser).filter(DBUser.id.in_(user_ids))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return query
                

def get_user_id_has(user_ids: List[int], db=Depends(get_db), query=Depends(get_all_query)) -> List[DBInfoBlock]:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBUser).filter(DBUser.id.in_(user_ids))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return db.scalars(query).all()
                

def get_user_has_query(users: List[SchemaBaseUser], query=Depends(get_all_query)) -> Select:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBUser).filter(DBUser.id.in_(map(lambda x: x.id, users)))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return query
                

def get_user_has(users: List[SchemaBaseUser], db=Depends(get_db), query=Depends(get_all_query)) -> List[DBInfoBlock]:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBUser).filter(DBUser.id.in_(map(lambda x: x.id, users)))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return db.scalars(query).all()
                

def get_certified_records_id_is_query(certified_record_id: int, query=Depends(get_all_query)) -> Select:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBCertifiedRecord).filter(DBCertifiedRecord.id.__eq__(certified_record_id))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return query
                

def get_certified_records_id_is(certified_record_id: int, db=Depends(get_db), query=Depends(get_all_query)) -> List[DBInfoBlock]:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBCertifiedRecord).filter(DBCertifiedRecord.id.__eq__(certified_record_id))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return db.scalars(query).all()
                

def get_certified_records_is_query(certified_record: SchemaBaseCertifiedRecord, query=Depends(get_all_query)) -> Select:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBCertifiedRecord).filter(DBCertifiedRecord.id.__eq__(certified_record.id))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return query
                

def get_certified_records_is(certified_record: SchemaBaseCertifiedRecord, db=Depends(get_db), query=Depends(get_all_query)) -> List[DBInfoBlock]:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBCertifiedRecord).filter(DBCertifiedRecord.id.__eq__(certified_record.id))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return db.scalars(query).all()
                

def get_certified_records_id_has_query(certified_record_ids: List[int], query=Depends(get_all_query)) -> Select:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBCertifiedRecord).filter(DBCertifiedRecord.id.in_(certified_record_ids))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return query
                

def get_certified_records_id_has(certified_record_ids: List[int], db=Depends(get_db), query=Depends(get_all_query)) -> List[DBInfoBlock]:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBCertifiedRecord).filter(DBCertifiedRecord.id.in_(certified_record_ids))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return db.scalars(query).all()
                

def get_certified_records_has_query(certified_records: List[SchemaBaseCertifiedRecord], query=Depends(get_all_query)) -> Select:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBCertifiedRecord).filter(DBCertifiedRecord.id.in_(map(lambda x: x.id, certified_records)))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return query
                

def get_certified_records_has(certified_records: List[SchemaBaseCertifiedRecord], db=Depends(get_db), query=Depends(get_all_query)) -> List[DBInfoBlock]:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBCertifiedRecord).filter(DBCertifiedRecord.id.in_(map(lambda x: x.id, certified_records)))
    query = query.options(joinedload(DBInfoBlock.user))
    query = query.options(selectinload(DBInfoBlock.certified_records))
    return db.scalars(query).all()
                
