# generate_hash: 339c8a05cdbdd0f9f8f05b1f7f517f4b
"""
This file was automatically generated in 2024-08-06 22:49:59.077905
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
async def get_one(ident: UUID4, db=Depends(get_db)) -> SchemaBaseTeacher:
    res = await db.get(DBTeacher, ident)
    if res:
        return res
    raise NOT_FOUND


async def __get_all_query(
        sort_by: Optional[str] = None, is_desc: bool = False,
) -> Select:
    query = select(DBTeacher)
    if sort_by is not None:
        if is_desc:
            query = query.order_by(getattr(DBTeacher, sort_by).desc())
        else:
            query = query.order_by(getattr(DBTeacher, sort_by))
    return query


async def get_all(
        query=Depends(__get_all_query),
        db=Depends(get_db)
) -> Page[SchemaBaseTeacher]:
    return await paginate(db, query)


async def get_link_all(
        query=Depends(__get_all_query),
        db=Depends(get_db)
) -> Page[SchemaTeacher]:
    return await paginate(db, query)
# ---------------------User Query Routes----------------------


# -----------------------Create Routes------------------------
async def create_one(
        course_ident: UUID4,
        response: Response, db=Depends(get_db)
) -> SchemaBaseTeacher:
    teacher = SchemaBaseTeacher(
    )
    teacher = DBTeacher(**teacher.model_dump())
    if course_ident is not None:
        course = await db.get(DBTeacher, course_ident)
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course Not found id:" + str(course_ident))
        teacher.fk_course_id = course_ident
    db.add(teacher)
    await db.commit()
    await db.refresh(teacher)
    response.status_code = status.HTTP_201_CREATED
    return SchemaBaseTeacher.model_validate(teacher)


# -----------------------Update Routes------------------------
async def update_one(
        ident: UUID4,
        db=Depends(get_db)) -> SchemaBaseTeacher:
    res = await db.get(DBTeacher, ident)
    if not res:
        raise NOT_FOUND
    await db.commit()
    await db.refresh(res)
    return SchemaBaseTeacher.model_validate(res)


# -----------------------Delete Routes------------------------
async def delete_one(ident: UUID4, db=Depends(get_db)):
    res = await db.get(DBTeacher, ident)
    if not res:
        raise NOT_FOUND
    res.course = None
    await db.commit()
    await db.delete(res)
    await db.commit()
    return {'message': 'Deleted', 'id': ident}


# ----------------------Relation Routes-----------------------
