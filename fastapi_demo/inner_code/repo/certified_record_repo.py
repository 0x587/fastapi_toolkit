# generate_hash: 659b6713fca95da3d17c11a2d433bd70
"""
This file was automatically generated in 2024-10-13 17:33:37.153299
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
def get_one(certified_record_ident: int, db=Depends(get_db)) -> DBCertifiedRecord:
    res = db.get(DBCertifiedRecord, certified_record_ident)
    if res and res.deleted_at is None:
        return res
    raise NOT_FOUND


def batch_get(certified_record_idents: List[int], db=Depends(get_db)) -> Page[SchemaBaseCertifiedRecord]:
    query = select(DBCertifiedRecord).filter(DBCertifiedRecord.deleted_at.is_(None)).filter(DBCertifiedRecord.id.in_(certified_record_idents))
    return paginate(db, query)

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
    target_real_name_like: Optional[str] = None
    self_real_name: Optional[str] = None
    self_real_name_like: Optional[str] = None
    relation: Optional[str] = None
    relation_like: Optional[str] = None
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


def get_all(
        query=Depends(get_all_query),
        db=Depends(get_db),
) -> Page[SchemaBaseCertifiedRecord]:
    return paginate(db, query)


def get_link_all(
        query=Depends(get_all_query),
        db=Depends(get_db)
) -> Page[SchemaCertifiedRecord]:
    return paginate(db, query)
# ---------------------User Query Routes----------------------


# -----------------------Create Routes------------------------
def create_one_model(model: SchemaBaseCertifiedRecord, db=Depends(get_db)) -> DBCertifiedRecord:
    certified_record = DBCertifiedRecord(**model.model_dump())
    db.add(certified_record)
    db.commit()
    db.refresh(certified_record)
    return certified_record

def create_one(
        done: bool,
        target_real_name: str,
        self_real_name: str,
        relation: str,
        _fk_user_user_id: Optional[int] = None,
        _fk_info_block_info_block_id: Optional[int] = None,
        db=Depends(get_db)
) -> DBCertifiedRecord:
    certified_record = DBCertifiedRecord(
        done=done,
        target_real_name=target_real_name,
        self_real_name=self_real_name,
        relation=relation,
        _fk_user_user_id=_fk_user_user_id,
        _fk_info_block_info_block_id=_fk_info_block_info_block_id,
        created_at=datetime.datetime.utcnow(),
        updated_at=datetime.datetime.utcnow(),
    )
    db.add(certified_record)
    db.commit()
    db.refresh(certified_record)
    return certified_record


# -----------------------Update Routes------------------------
class ForceUpdate(BaseModel):
    done: Optional[bool] = Field(default=False)
    target_real_name: Optional[bool] = Field(default=False)
    self_real_name: Optional[bool] = Field(default=False)
    relation: Optional[bool] = Field(default=False)

def update_one(
        certified_record_ident: int,
        done: Optional[bool] = None,
        target_real_name: Optional[str] = None,
        self_real_name: Optional[str] = None,
        relation: Optional[str] = None,
        force_update: Optional[ForceUpdate] = ForceUpdate(),
        db=Depends(get_db)) -> DBCertifiedRecord:
    res = db.get(DBCertifiedRecord, certified_record_ident)
    if not res or res.deleted_at is not None:
        raise NOT_FOUND
    if done is not None or force_update.done:
        res.done = done
    if target_real_name is not None or force_update.target_real_name:
        res.target_real_name = target_real_name
    if self_real_name is not None or force_update.self_real_name:
        res.self_real_name = self_real_name
    if relation is not None or force_update.relation:
        res.relation = relation
    res.updated_at = datetime.datetime.now()
    db.commit()
    db.refresh(res)
    return SchemaBaseCertifiedRecord.model_validate(res)


# -----------------------Delete Routes------------------------
def delete_one(certified_record_ident: int, db=Depends(get_db)):
    res = db.get(DBCertifiedRecord, certified_record_ident)
    if not res or res.deleted_at is not None:
        raise NOT_FOUND
# TODO
    res.deleted_at = datetime.datetime.now()
    db.commit()
    return {'message': 'Deleted', 'id': certified_record_ident}


# ----------------------Relation Routes-----------------------


def get_user_id_is_query(user_id: int, query=Depends(get_all_query)) -> Select:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBUser).filter(DBUser.id.__eq__(user_id))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return query
                

def get_user_id_is(user_id: int, db=Depends(get_db), query=Depends(get_all_query)) -> List[DBCertifiedRecord]:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBUser).filter(DBUser.id.__eq__(user_id))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return db.scalars(query).all()
                

def get_user_is_query(user: SchemaBaseUser, query=Depends(get_all_query)) -> Select:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBUser).filter(DBUser.id.__eq__(user.id))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return query
                

def get_user_is(user: SchemaBaseUser, db=Depends(get_db), query=Depends(get_all_query)) -> List[DBCertifiedRecord]:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBUser).filter(DBUser.id.__eq__(user.id))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return db.scalars(query).all()
                

def get_user_id_has_query(user_ids: List[int], query=Depends(get_all_query)) -> Select:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBUser).filter(DBUser.id.in_(user_ids))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return query
                

def get_user_id_has(user_ids: List[int], db=Depends(get_db), query=Depends(get_all_query)) -> List[DBCertifiedRecord]:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBUser).filter(DBUser.id.in_(user_ids))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return db.scalars(query).all()
                

def get_user_has_query(users: List[SchemaBaseUser], query=Depends(get_all_query)) -> Select:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBUser).filter(DBUser.id.in_(map(lambda x: x.id, users)))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return query
                

def get_user_has(users: List[SchemaBaseUser], db=Depends(get_db), query=Depends(get_all_query)) -> List[DBCertifiedRecord]:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBUser).filter(DBUser.id.in_(map(lambda x: x.id, users)))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return db.scalars(query).all()
                

def get_info_block_id_is_query(info_block_id: int, query=Depends(get_all_query)) -> Select:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBInfoBlock).filter(DBInfoBlock.id.__eq__(info_block_id))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return query
                

def get_info_block_id_is(info_block_id: int, db=Depends(get_db), query=Depends(get_all_query)) -> List[DBCertifiedRecord]:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBInfoBlock).filter(DBInfoBlock.id.__eq__(info_block_id))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return db.scalars(query).all()
                

def get_info_block_is_query(info_block: SchemaBaseInfoBlock, query=Depends(get_all_query)) -> Select:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBInfoBlock).filter(DBInfoBlock.id.__eq__(info_block.id))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return query
                

def get_info_block_is(info_block: SchemaBaseInfoBlock, db=Depends(get_db), query=Depends(get_all_query)) -> List[DBCertifiedRecord]:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBInfoBlock).filter(DBInfoBlock.id.__eq__(info_block.id))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return db.scalars(query).all()
                

def get_info_block_id_has_query(info_block_ids: List[int], query=Depends(get_all_query)) -> Select:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBInfoBlock).filter(DBInfoBlock.id.in_(info_block_ids))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return query
                

def get_info_block_id_has(info_block_ids: List[int], db=Depends(get_db), query=Depends(get_all_query)) -> List[DBCertifiedRecord]:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBInfoBlock).filter(DBInfoBlock.id.in_(info_block_ids))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return db.scalars(query).all()
                

def get_info_block_has_query(info_blocks: List[SchemaBaseInfoBlock], query=Depends(get_all_query)) -> Select:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBInfoBlock).filter(DBInfoBlock.id.in_(map(lambda x: x.id, info_blocks)))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return query
                

def get_info_block_has(info_blocks: List[SchemaBaseInfoBlock], db=Depends(get_db), query=Depends(get_all_query)) -> List[DBCertifiedRecord]:
    if type(query) is not Select:
        query = get_all_query(QueryParams())
    query = query.join(DBInfoBlock).filter(DBInfoBlock.id.in_(map(lambda x: x.id, info_blocks)))
    query = query.options(joinedload(DBCertifiedRecord.user))
    query = query.options(joinedload(DBCertifiedRecord.info_block))
    return db.scalars(query).all()
                
