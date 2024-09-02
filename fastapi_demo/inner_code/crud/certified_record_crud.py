# generate_hash: 5101e6f80b990ecc65e5e646621ec508
"""
This file was automatically generated in 2024-09-02 21:56:14.802685
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
async def get_one(ident: int, db=Depends(get_db)) -> SchemaBaseCertifiedRecord:
    res = await db.get(DBCertifiedRecord, ident)
    if res and res.deleted_at is None:
        return res
    raise NOT_FOUND


async def batch_get(idents: List[int], db=Depends(get_db)) -> Page[SchemaBaseCertifiedRecord]:
    query = select(DBCertifiedRecord).filter(DBCertifiedRecord.deleted_at.is_(None)).filter(DBCertifiedRecord.id.in_(idents))
    return await paginate(db, query)


def get_all_query(
        filter_done: Optional[bool] = None,
        filter_target_real_name: Optional[str] = None,
        filter_self_real_name: Optional[str] = None,
        filter_relation: Optional[str] = None,
        sort_by: Optional[str] = None, is_desc: bool = False,
) -> Select:
    query = select(DBCertifiedRecord).filter(DBCertifiedRecord.deleted_at.is_(None))
    if filter_done is not None:
        query = query.filter(DBCertifiedRecord.done.__eq__(filter_done))
    if filter_target_real_name is not None:
        query = query.filter(DBCertifiedRecord.target_real_name.__eq__(filter_target_real_name))
    if filter_self_real_name is not None:
        query = query.filter(DBCertifiedRecord.self_real_name.__eq__(filter_self_real_name))
    if filter_relation is not None:
        query = query.filter(DBCertifiedRecord.relation.__eq__(filter_relation))
    if sort_by is not None:
        if is_desc:
            query = query.order_by(getattr(DBCertifiedRecord, sort_by).desc())
        else:
            query = query.order_by(getattr(DBCertifiedRecord, sort_by))
    return query


async def get_all(
        paginate_parmas: Params,
        query=Depends(get_all_query),
        db=Depends(get_db),
) -> Page[SchemaBaseCertifiedRecord]:
    return await paginate(db, query, params=paginate_parmas)


async def get_link_all(
        paginate_parmas: Params,
        query=Depends(get_all_query),
        db=Depends(get_db)
) -> Page[SchemaCertifiedRecord]:
    return await paginate(db, query, params=paginate_parmas)
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
        ident: int,
        done: Optional[bool] = None,
        target_real_name: Optional[str] = None,
        self_real_name: Optional[str] = None,
        relation: Optional[str] = None,
        db=Depends(get_db)) -> SchemaBaseCertifiedRecord:
    res = await db.get(DBCertifiedRecord, ident)
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
async def delete_one(ident: int, db=Depends(get_db)):
    res = await db.get(DBCertifiedRecord, ident)
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
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return query
                

async def get_user_id_is(user_id: int, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaCertifiedRecord]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBUser).filter(DBUser.id.__eq__(user_id))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return (await db.scalars(query)).all()
                

def get_user_is_query(user: SchemaBaseUser) -> Select:
    query = get_all_query()
    query = query.join(DBUser).filter(DBUser.id.__eq__(user.id))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return query
                

async def get_user_is(user: SchemaBaseUser, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaCertifiedRecord]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBUser).filter(DBUser.id.__eq__(user.id))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return (await db.scalars(query)).all()
                

def get_user_id_has_query(user_ids: List[int]) -> Select:
    query = get_all_query()
    query = query.join(DBUser).filter(DBUser.id.in_(user_ids))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return query
                

async def get_user_id_has(user_ids: List[int], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaCertifiedRecord]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBUser).filter(DBUser.id.in_(user_ids))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return (await db.scalars(query)).all()
                

def get_user_has_query(users: List[SchemaBaseUser]) -> Select:
    query = get_all_query()
    query = query.join(DBUser).filter(DBUser.id.in_(map(lambda x: x.id, users)))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return query
                

async def get_user_has(users: List[SchemaBaseUser], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaCertifiedRecord]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBUser).filter(DBUser.id.in_(map(lambda x: x.id, users)))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return (await db.scalars(query)).all()
                

def get_info_block_id_is_query(info_block_id: int) -> Select:
    query = get_all_query()
    query = query.join(DBInfoBlock).filter(DBInfoBlock.id.__eq__(info_block_id))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return query
                

async def get_info_block_id_is(info_block_id: int, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaCertifiedRecord]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBInfoBlock).filter(DBInfoBlock.id.__eq__(info_block_id))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return (await db.scalars(query)).all()
                

def get_info_block_is_query(info_block: SchemaBaseInfoBlock) -> Select:
    query = get_all_query()
    query = query.join(DBInfoBlock).filter(DBInfoBlock.id.__eq__(info_block.id))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return query
                

async def get_info_block_is(info_block: SchemaBaseInfoBlock, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaCertifiedRecord]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBInfoBlock).filter(DBInfoBlock.id.__eq__(info_block.id))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return (await db.scalars(query)).all()
                

def get_info_block_id_has_query(info_block_ids: List[int]) -> Select:
    query = get_all_query()
    query = query.join(DBInfoBlock).filter(DBInfoBlock.id.in_(info_block_ids))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return query
                

async def get_info_block_id_has(info_block_ids: List[int], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaCertifiedRecord]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBInfoBlock).filter(DBInfoBlock.id.in_(info_block_ids))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return (await db.scalars(query)).all()
                

def get_info_block_has_query(info_blocks: List[SchemaBaseInfoBlock]) -> Select:
    query = get_all_query()
    query = query.join(DBInfoBlock).filter(DBInfoBlock.id.in_(map(lambda x: x.id, info_blocks)))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return query
                

async def get_info_block_has(info_blocks: List[SchemaBaseInfoBlock], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaCertifiedRecord]:
    if type(query) is not Select:
        query = get_all_query()
    query = query.join(DBInfoBlock).filter(DBInfoBlock.id.in_(map(lambda x: x.id, info_blocks)))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return (await db.scalars(query)).all()
                
