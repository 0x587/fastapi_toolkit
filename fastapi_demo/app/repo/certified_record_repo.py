# generate_hash: 718b37da94998b00d8942739164f5343
"""
This file was automatically generated in 2024-09-29 00:28:32.145667
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

NOT_FOUND = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item Not found")


# ------------------------Query Routes------------------------
def get_one(certified_record_ident: int, db=Depends(get_db)) -> CertifiedRecord:
    res = db.get(CertifiedRecord, certified_record_ident)
    if res and res.deleted_at is None:
        return res
    raise NOT_FOUND


def batch_get(certified_record_idents: List[int], db=Depends(get_db)) -> Page[CertifiedRecord]:
    query = select(CertifiedRecord).filter(CertifiedRecord.deleted_at.is_(None)).filter(CertifiedRecord.id.in_(certified_record_idents))
    return paginate(db, query)

class QueryParams(BaseModel):
    class SortParams(BaseModel):
        class StorFieldEnum(str, Enum):
            id = "id"
            done = "done"
            target_real_name = "target_real_name"
            self_real_name = "self_real_name"
            relation = "relation"

        field: StorFieldEnum
        is_desc: bool = False

    id: Optional[int] = None,
    done: Optional[bool] = None,
    target_real_name: Optional[str] = None,
    target_real_name_like: Optional[str] = None,
    self_real_name: Optional[str] = None,
    self_real_name_like: Optional[str] = None,
    relation: Optional[str] = None,
    relation_like: Optional[str] = None,
    sort_by: List[SortParams] = Field(default_factory=list)

def get_all_query(params: QueryParams = Body()) -> Select:
    query = select(CertifiedRecord).filter(CertifiedRecord.deleted_at.is_(None))
    if params.id is not None:
        query = query.filter(CertifiedRecord.id.__eq__(params.id))
    if params.done is not None:
        query = query.filter(CertifiedRecord.done.__eq__(params.done))
    if params.target_real_name is not None:
        query = query.filter(CertifiedRecord.target_real_name.__eq__(params.target_real_name))
    if params.target_real_name_like is not None:
        query = query.filter(CertifiedRecord.target_real_name.like(params.target_real_name_like))
    if params.self_real_name is not None:
        query = query.filter(CertifiedRecord.self_real_name.__eq__(params.self_real_name))
    if params.self_real_name_like is not None:
        query = query.filter(CertifiedRecord.self_real_name.like(params.self_real_name_like))
    if params.relation is not None:
        query = query.filter(CertifiedRecord.relation.__eq__(params.relation))
    if params.relation_like is not None:
        query = query.filter(CertifiedRecord.relation.like(params.relation_like))
    for sort_item in params.sort_by:
        if sort_item.is_desc:
            query = query.order_by(getattr(CertifiedRecord, sort_item.field).desc())
        else:
            query = query.order_by(getattr(CertifiedRecord, sort_item.field))
    return query


def get_all(
        query=Depends(get_all_query),
        db=Depends(get_db),
) -> Page[CertifiedRecord]:
    return paginate(db, query)

# ---------------------User Query Routes----------------------


# -----------------------Create Routes------------------------
def create_one_model(model: CertifiedRecord, db=Depends(get_db)) -> CertifiedRecord:
    certified_record = CertifiedRecord(**model.model_dump())
    db.add(certified_record)
    db.commit()
    db.refresh(certified_record)
    return certified_record

def create_one(
        id: int,
        done: bool,
        target_real_name: str,
        self_real_name: str,
        relation: str,
        db=Depends(get_db)
) -> CertifiedRecord:
    certified_record = CertifiedRecord(
        id=id,
        done=done,
        target_real_name=target_real_name,
        self_real_name=self_real_name,
        relation=relation,
    )
    return create_one_model(certified_record, db)


# -----------------------Update Routes------------------------
def update_one(
        certified_record_ident: int,
        id: Optional[int] = None,
        done: Optional[bool] = None,
        target_real_name: Optional[str] = None,
        self_real_name: Optional[str] = None,
        relation: Optional[str] = None,
        db=Depends(get_db)) -> CertifiedRecord:
    res = db.get(CertifiedRecord, certified_record_ident)
    if not res or res.deleted_at is not None:
        raise NOT_FOUND
    if id is not None:
        res.id = id
    if done is not None:
        res.done = done
    if target_real_name is not None:
        res.target_real_name = target_real_name
    if self_real_name is not None:
        res.self_real_name = self_real_name
    if relation is not None:
        res.relation = relation
    res.updated_at = datetime.datetime.now()
    db.commit()
    db.refresh(res)
    return CertifiedRecord.model_validate(res)


# -----------------------Delete Routes------------------------
def delete_one(certified_record_ident: int, db=Depends(get_db)):
    res = db.get(CertifiedRecord, certified_record_ident)
    if not res or res.deleted_at is not None:
        raise NOT_FOUND
# TODO
    res.deleted_at = datetime.datetime.now()
    db.commit()
    return {'message': 'Deleted', 'id': certified_record_ident}


# ----------------------Relation Routes-----------------------

