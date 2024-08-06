# generate_hash: 8f7753d276bb514e3f212608c765672d
"""
This file was automatically generated in 2024-08-06 22:49:59.077459
"""

from typing import List, Optional
from fastapi import Depends, Response, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.async_sqlalchemy import paginate
from pydantic import UUID4
import uuid
import datetime
from sqlalchemy import select, Select
from ..db import get_db
from ..models import *
from ..schemas import *

NOT_FOUND = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item Not found")


# ------------------------Query Routes------------------------
async def get_one(ident: UUID4, db=Depends(get_db)) -> SchemaBaseStudent:
    res = await db.get(DBStudent, ident)
    if res:
        return res
    raise NOT_FOUND


async def __get_all_query(
        filter_name: Optional[str] = None,
        filter_mode: Optional[StudentMode] = None,
        sort_by: Optional[str] = None, is_desc: bool = False,
) -> Select:
    query = select(DBStudent)
    if filter_name is not None:
        query = query.filter(DBStudent.name == filter_name)
    if filter_mode is not None:
        query = query.filter(DBStudent.mode == filter_mode)
    if sort_by is not None:
        if is_desc:
            query = query.order_by(getattr(DBStudent, sort_by).desc())
        else:
            query = query.order_by(getattr(DBStudent, sort_by))
    return query


async def get_all(
        query=Depends(__get_all_query),
        db=Depends(get_db)
) -> Page[SchemaBaseStudent]:
    return await paginate(db, query)


async def get_link_all(
        query=Depends(__get_all_query),
        db=Depends(get_db)
) -> Page[SchemaStudent]:
    return await paginate(db, query)
# ---------------------User Query Routes----------------------


# -----------------------Create Routes------------------------
async def create_one(
        name: str,
        mode: StudentMode,
        response: Response, db=Depends(get_db)
) -> SchemaBaseStudent:
    student = SchemaBaseStudent(
        name=name,
        mode=mode,
    )
    student = DBStudent(**student.model_dump())
    db.add(student)
    await db.commit()
    await db.refresh(student)
    response.status_code = status.HTTP_201_CREATED
    return SchemaBaseStudent.model_validate(student)


# -----------------------Update Routes------------------------
async def update_one(
        ident: UUID4,
        name: Optional[str] = None,
        mode: Optional[StudentMode] = None,
        db=Depends(get_db)) -> SchemaBaseStudent:
    res = await db.get(DBStudent, ident)
    if not res:
        raise NOT_FOUND
    if name is not None:
        res.name = name
    if mode is not None:
        res.mode = mode
    await db.commit()
    await db.refresh(res)
    return SchemaBaseStudent.model_validate(res)


# -----------------------Delete Routes------------------------
async def delete_one(ident: UUID4, db=Depends(get_db)):
    res = await db.get(DBStudent, ident)
    if not res:
        raise NOT_FOUND
    for i in await res.awaitable_attrs.grades:
        await db.delete(i)
    await db.commit()
    await db.delete(res)
    await db.commit()
    return {'message': 'Deleted', 'id': ident}


# ----------------------Relation Routes-----------------------
