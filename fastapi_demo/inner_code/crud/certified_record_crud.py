# generate_hash: 6901dada59925f6b234903c3e15f8b96
"""
This file was automatically generated in 2024-09-04 16:25:51.563902
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
async def get_one(certified_record_ident: int, db=Depends(get_db)) -> SchemaBaseCertifiedRecord:
    res = await db.get(DBCertifiedRecord, certified_record_ident)
    if res and res.deleted_at is None:
        return res
    raise NOT_FOUND


async def batch_get(certified_record_idents: List[int], db=Depends(get_db)) -> Page[SchemaBaseCertifiedRecord]:
    query = select(DBCertifiedRecord).filter(DBCertifiedRecord.deleted_at.is_(None)).filter(DBCertifiedRecord.id.in_(certified_record_idents))
    return await paginate(db, query)

class QueryParams(BaseModel):
    class SortParams(BaseModel):
        class StorFieldEnum(str, Enum):
            done = "done"
            target_real_name = "target_real_name"
            self_real_name = "self_real_name"
            relation = "relation"

        field: StorFieldEnum
        is_desc: bool = False

    done: Optional[bool] = None
    target_real_name: Optional[str] = None
    target_real_name_like = None
    self_real_name: Optional[str] = None
    self_real_name_like = None
    relation: Optional[str] = None
    relation_like = None
    sort_by: List[SortParams] = Field(default_factory=list)

def get_all_query(params: QueryParams = Body()) -> Select:
    query = select(DBCertifiedRecord).filter(DBCertifiedRecord.deleted_at.is_(None))
    if params.done is not None:
        query = query.filter(DBCertifiedRecord.done.__eq__(params.done))
    if params.target_real_name is not None:
        query = query.filter(DBCertifiedRecord.target_real_name.__eq__(params.target_real_name))
    if params.target_real_name_like is not None:
        query = query.filter(DBCertifiedRecord.target_real_name.like(params.target_real_name_like))
    if params.self_real_name is not None:
        query = query.filter(DBCertifiedRecord.self_real_name.__eq__(params.self_real_name))
    if params.self_real_name_like is not None:
        query = query.filter(DBCertifiedRecord.self_real_name.like(params.self_real_name_like))
    if params.relation is not None:
        query = query.filter(DBCertifiedRecord.relation.__eq__(params.relation))
    if params.relation_like is not None:
        query = query.filter(DBCertifiedRecord.relation.like(params.relation_like))
    for sort_item in params.sort_by:
        if sort_item.is_desc:
            query = query.order_by(getattr(DBCertifiedRecord, sort_item.field).desc())
        else:
            query = query.order_by(getattr(DBCertifiedRecord, sort_item.field))
    return query


async def get_all(
        query=Depends(get_all_query),
        db=Depends(get_db),
) -> Page[SchemaBaseCertifiedRecord]:
    return await paginate(db, query)


async def get_link_all(
        query=Depends(get_all_query),
        db=Depends(get_db)
) -> Page[SchemaCertifiedRecord]:
    return await paginate(db, query)
# ---------------------User Query Routes----------------------


# -----------------------Create Routes------------------------
async def create_one(
        done: bool,
        target_real_name: str,
        self_real_name: str,
        relation: str,
        db=Depends(get_db)
) -> SchemaBaseCertifiedRecord:
    certified_record = SchemaBaseCertifiedRecord(
        done=done,
        target_real_name=target_real_name,
        self_real_name=self_real_name,
        relation=relation,
    )
    certified_record = DBCertifiedRecord(**certified_record.model_dump())
    db.add(certified_record)
    await db.commit()
    await db.refresh(certified_record)
    return SchemaBaseCertifiedRecord.model_validate(certified_record)


# -----------------------Update Routes------------------------
async def update_one(
        certified_record_ident: int,
        done: Optional[bool] = None,
        target_real_name: Optional[str] = None,
        self_real_name: Optional[str] = None,
        relation: Optional[str] = None,
        db=Depends(get_db)) -> SchemaBaseCertifiedRecord:
    res = await db.get(DBCertifiedRecord, certified_record_ident)
    if not res or res.deleted_at is not None:
        raise NOT_FOUND
    if done is not None:
        res.done = done
    if target_real_name is not None:
        res.target_real_name = target_real_name
    if self_real_name is not None:
        res.self_real_name = self_real_name
    if relation is not None:
        res.relation = relation
    res.updated_at = datetime.datetime.now()
    await db.commit()
    await db.refresh(res)
    return SchemaBaseCertifiedRecord.model_validate(res)


# -----------------------Delete Routes------------------------
async def delete_one(certified_record_ident: int, db=Depends(get_db)):
    res = await db.get(DBCertifiedRecord, certified_record_ident)
    if not res or res.deleted_at is not None:
        raise NOT_FOUND
# TODO
    res.deleted_at = datetime.datetime.now()
    await db.commit()
    return {'message': 'Deleted', 'id': certified_record_ident}


# ----------------------Relation Routes-----------------------


def get_user_id_is_query(self, user_id: int) -> Select:
    query = self.get_all_query()
    query = query.join(DBUser).filter(DBUser.id.__eq__(user_id))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return query
                

async def get_user_id_is(self, user_id: int, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaCertifiedRecord]:
    if type(query) is not Select:
        query = self.get_all_query()
    query = query.join(DBUser).filter(DBUser.id.__eq__(user_id))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return (await db.scalars(query)).all()
                

def get_user_is_query(self, user: SchemaBaseUser) -> Select:
    query = self.get_all_query()
    query = query.join(DBUser).filter(DBUser.id.__eq__(user.id))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return query
                

async def get_user_is(self, user: SchemaBaseUser, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaCertifiedRecord]:
    if type(query) is not Select:
        query = self.get_all_query()
    query = query.join(DBUser).filter(DBUser.id.__eq__(user.id))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return (await db.scalars(query)).all()
                

def get_user_id_has_query(self, user_ids: List[int]) -> Select:
    query = self.get_all_query()
    query = query.join(DBUser).filter(DBUser.id.in_(user_ids))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return query
                

async def get_user_id_has(self, user_ids: List[int], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaCertifiedRecord]:
    if type(query) is not Select:
        query = self.get_all_query()
    query = query.join(DBUser).filter(DBUser.id.in_(user_ids))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return (await db.scalars(query)).all()
                

def get_user_has_query(self, users: List[SchemaBaseUser]) -> Select:
    query = self.get_all_query()
    query = query.join(DBUser).filter(DBUser.id.in_(map(lambda x: x.id, users)))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return query
                

async def get_user_has(self, users: List[SchemaBaseUser], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaCertifiedRecord]:
    if type(query) is not Select:
        query = self.get_all_query()
    query = query.join(DBUser).filter(DBUser.id.in_(map(lambda x: x.id, users)))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return (await db.scalars(query)).all()
                

def get_info_block_id_is_query(self, info_block_id: int) -> Select:
    query = self.get_all_query()
    query = query.join(DBInfoBlock).filter(DBInfoBlock.id.__eq__(info_block_id))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return query
                

async def get_info_block_id_is(self, info_block_id: int, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaCertifiedRecord]:
    if type(query) is not Select:
        query = self.get_all_query()
    query = query.join(DBInfoBlock).filter(DBInfoBlock.id.__eq__(info_block_id))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return (await db.scalars(query)).all()
                

def get_info_block_is_query(self, info_block: SchemaBaseInfoBlock) -> Select:
    query = self.get_all_query()
    query = query.join(DBInfoBlock).filter(DBInfoBlock.id.__eq__(info_block.id))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return query
                

async def get_info_block_is(self, info_block: SchemaBaseInfoBlock, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaCertifiedRecord]:
    if type(query) is not Select:
        query = self.get_all_query()
    query = query.join(DBInfoBlock).filter(DBInfoBlock.id.__eq__(info_block.id))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return (await db.scalars(query)).all()
                

def get_info_block_id_has_query(self, info_block_ids: List[int]) -> Select:
    query = self.get_all_query()
    query = query.join(DBInfoBlock).filter(DBInfoBlock.id.in_(info_block_ids))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return query
                

async def get_info_block_id_has(self, info_block_ids: List[int], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaCertifiedRecord]:
    if type(query) is not Select:
        query = self.get_all_query()
    query = query.join(DBInfoBlock).filter(DBInfoBlock.id.in_(info_block_ids))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return (await db.scalars(query)).all()
                

def get_info_block_has_query(self, info_blocks: List[SchemaBaseInfoBlock]) -> Select:
    query = self.get_all_query()
    query = query.join(DBInfoBlock).filter(DBInfoBlock.id.in_(map(lambda x: x.id, info_blocks)))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return query
                

async def get_info_block_has(self, info_blocks: List[SchemaBaseInfoBlock], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaCertifiedRecord]:
    if type(query) is not Select:
        query = self.get_all_query()
    query = query.join(DBInfoBlock).filter(DBInfoBlock.id.in_(map(lambda x: x.id, info_blocks)))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return (await db.scalars(query)).all()
                
