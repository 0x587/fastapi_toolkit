from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from fastapi import Depends, Body, Response, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
import datetime
from sqlalchemy import Select
from sqlmodel import select
from sqlalchemy.orm import joinedload, selectinload
from ..db import get_db_sync as get_db
from ..models import *

NOT_FOUND = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item Not found")


# ------------------------Query Routes------------------------
def get_one(info_block_ident: int, db=Depends(get_db)) -> InfoBlock:
    res = db.get(InfoBlock, info_block_ident)
    if res and res.deleted_at is None:
        return res
    raise NOT_FOUND


def batch_get(info_block_idents: List[int], db=Depends(get_db)) -> List[InfoBlock]:
    query = select(InfoBlock).filter(InfoBlock.deleted_at.is_(None)).filter(InfoBlock.id.in_(info_block_idents))
    return db.scalars(query).all()

class QueryParams(BaseModel):
    class SortParams(BaseModel):
        class StorFieldEnum(str, Enum):
            type = "type"
            title = "title"
            sub_title = "sub_title"
            tags = "tags"
            show = "show"
            desc = "desc"
            time_start = "time_start"
            time_end = "time_end"

        field: StorFieldEnum
        is_desc: bool = False

    type: Optional[str] = None
    type_like: Optional[str] = None
    title: Optional[str] = None
    title_like: Optional[str] = None
    sub_title: Optional[str] = None
    sub_title_like: Optional[str] = None
    tags: Optional[str] = None
    tags_like: Optional[str] = None
    show: Optional[bool] = None
    desc: Optional[str] = None
    desc_like: Optional[str] = None
    time_start: Optional[datetime.date] = None
    time_end: Optional[datetime.date] = None
    sort_by: List[SortParams] = Field(default_factory=list)

def get_all_query(params: QueryParams = Body()) -> Select:
    query = select(InfoBlock).where(InfoBlock.deleted_at.is_(None))
    if params.type is not None:
        query = query.where(InfoBlock.type == params.type)
    if params.type_like is not None:
        query = query.where(InfoBlock.type.like(params.type_like))
    if params.title is not None:
        query = query.where(InfoBlock.title == params.title)
    if params.title_like is not None:
        query = query.where(InfoBlock.title.like(params.title_like))
    if params.sub_title is not None:
        query = query.where(InfoBlock.sub_title == params.sub_title)
    if params.sub_title_like is not None:
        query = query.where(InfoBlock.sub_title.like(params.sub_title_like))
    if params.tags is not None:
        query = query.where(InfoBlock.tags == params.tags)
    if params.tags_like is not None:
        query = query.where(InfoBlock.tags.like(params.tags_like))
    if params.show is not None:
        query = query.where(InfoBlock.show == params.show)
    if params.desc is not None:
        query = query.where(InfoBlock.desc == params.desc)
    if params.time_start is not None:
        query = query.where(InfoBlock.time_start == params.time_start)
    if params.time_end is not None:
        query = query.where(InfoBlock.time_end == params.time_end)
    for sort_item in params.sort_by:
        if sort_item.is_desc:
            query = query.order_by(getattr(InfoBlock, sort_item.field).desc())
        else:
            query = query.order_by(getattr(InfoBlock, sort_item.field))
    return query


def get_all(
        query=Depends(get_all_query),
        db=Depends(get_db),
) -> Page[InfoBlock]:
    return paginate(db, query)

# ---------------------User Query Routes----------------------


# -----------------------Create Routes------------------------
def create_one_model(model: InfoBlock, db=Depends(get_db)) -> InfoBlock:
    info_block = InfoBlock(**model.model_dump())
    db.add(info_block)
    db.commit()
    db.refresh(info_block)
    return info_block

def create_one(
        type: str,
        title: str,
        sub_title: str,
        tags: str,
        show: bool,
        desc: Optional[str] = None,
        time_start: Optional[datetime.date] = None,
        time_end: Optional[datetime.date] = None,
        db=Depends(get_db)
) -> InfoBlock:
    info_block = InfoBlock(
        type=type,
        title=title,
        sub_title=sub_title,
        tags=tags,
        show=show,
        desc=desc,
        time_start=time_start,
        time_end=time_end,
    )
    return create_one_model(info_block, db)


# -----------------------Update Routes------------------------
def update_one(
        info_block_ident: int,
        type: Optional[str] = None,
        title: Optional[str] = None,
        sub_title: Optional[str] = None,
        tags: Optional[str] = None,
        show: Optional[bool] = None,
        desc: Optional[str] = None,
        time_start: Optional[datetime.date] = None,
        time_end: Optional[datetime.date] = None,
        db=Depends(get_db)) -> InfoBlock:
    res = db.get(InfoBlock, info_block_ident)
    if not res or res.deleted_at is not None:
        raise NOT_FOUND
    if type is not None:
        res.type = type
    if title is not None:
        res.title = title
    if sub_title is not None:
        res.sub_title = sub_title
    if tags is not None:
        res.tags = tags
    if show is not None:
        res.show = show
    if desc is not None:
        res.desc = desc
    if time_start is not None:
        res.time_start = time_start
    if time_end is not None:
        res.time_end = time_end
    res.updated_at = datetime.datetime.now()
    db.commit()
    db.refresh(res)
    return InfoBlock.model_validate(res)


# -----------------------Delete Routes------------------------
def delete_one(info_block_ident: int, db=Depends(get_db)):
    res = db.get(InfoBlock, info_block_ident)
    if not res or res.deleted_at is not None:
        raise NOT_FOUND
# TODO
    res.deleted_at = datetime.datetime.now()
    db.commit()
    return {'message': 'Deleted', 'id': info_block_ident}


# ----------------------Relation Routes-----------------------

