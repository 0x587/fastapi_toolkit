# generate_hash: 9b5a6f054e3d16c807f0935b11ec312c
"""
This file was automatically generated in 2024-08-06 22:49:59.077690
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
async def get_one(ident: UUID4, db=Depends(get_db)) -> SchemaBaseCourse:
    res = await db.get(DBCourse, ident)
    if res:
        return res
    raise NOT_FOUND


async def __get_all_query(
        filter_name: Optional[str] = None,
        sort_by: Optional[str] = None, is_desc: bool = False,
) -> Select:
    query = select(DBCourse)
    if filter_name is not None:
        query = query.filter(DBCourse.name == filter_name)
    if sort_by is not None:
        if is_desc:
            query = query.order_by(getattr(DBCourse, sort_by).desc())
        else:
            query = query.order_by(getattr(DBCourse, sort_by))
    return query


async def get_all(
        query=Depends(__get_all_query),
        db=Depends(get_db)
) -> Page[SchemaBaseCourse]:
    return await paginate(db, query)


async def get_link_all(
        query=Depends(__get_all_query),
        db=Depends(get_db)
) -> Page[SchemaCourse]:
    return await paginate(db, query)
# ---------------------User Query Routes----------------------


# -----------------------Create Routes------------------------
async def create_one(
        name: str,
        response: Response, db=Depends(get_db)
) -> SchemaBaseCourse:
    course = SchemaBaseCourse(
        name=name,
    )
    course = DBCourse(**course.model_dump())
    db.add(course)
    await db.commit()
    await db.refresh(course)
    response.status_code = status.HTTP_201_CREATED
    return SchemaBaseCourse.model_validate(course)


# -----------------------Update Routes------------------------
async def update_one(
        ident: UUID4,
        name: Optional[str] = None,
        db=Depends(get_db)) -> SchemaBaseCourse:
    res = await db.get(DBCourse, ident)
    if not res:
        raise NOT_FOUND
    if name is not None:
        res.name = name
    await db.commit()
    await db.refresh(res)
    return SchemaBaseCourse.model_validate(res)


# -----------------------Delete Routes------------------------
async def delete_one(ident: UUID4, db=Depends(get_db)):
    res = await db.get(DBCourse, ident)
    if not res:
        raise NOT_FOUND
    for i in await res.awaitable_attrs.grades:
        await db.delete(i)
    for i in await res.awaitable_attrs.teachers:
        await db.delete(i)
    await db.commit()
    await db.delete(res)
    await db.commit()
    return {'message': 'Deleted', 'id': ident}


# ----------------------Relation Routes-----------------------
