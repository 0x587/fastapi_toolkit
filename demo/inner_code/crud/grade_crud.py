# generate_hash: 3ab49a17033815ee0e8af9afe0c89172
"""
This file was automatically generated in 2024-08-06 22:49:59.078132
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
async def get_one(ident: UUID4, db=Depends(get_db)) -> SchemaBaseGrade:
    res = await db.get(DBGrade, ident)
    if res:
        return res
    raise NOT_FOUND


async def __get_all_query(
        filter_grade: Optional[float] = None,
        sort_by: Optional[str] = None, is_desc: bool = False,
) -> Select:
    query = select(DBGrade)
    if filter_grade is not None:
        query = query.filter(DBGrade.grade == filter_grade)
    if sort_by is not None:
        if is_desc:
            query = query.order_by(getattr(DBGrade, sort_by).desc())
        else:
            query = query.order_by(getattr(DBGrade, sort_by))
    return query


async def get_all(
        query=Depends(__get_all_query),
        db=Depends(get_db)
) -> Page[SchemaBaseGrade]:
    return await paginate(db, query)


async def get_link_all(
        query=Depends(__get_all_query),
        db=Depends(get_db)
) -> Page[SchemaGrade]:
    return await paginate(db, query)
# ---------------------User Query Routes----------------------


# -----------------------Create Routes------------------------
async def create_one(
        grade: float,
        student_ident: UUID4,
        course_ident: UUID4,
        response: Response, db=Depends(get_db)
) -> SchemaBaseGrade:
    grade = SchemaBaseGrade(
        grade=grade,
    )
    grade = DBGrade(**grade.model_dump())
    if student_ident is not None:
        student = await db.get(DBGrade, student_ident)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student Not found id:" + str(student_ident))
        grade.fk_student_id = student_ident
    if course_ident is not None:
        course = await db.get(DBGrade, course_ident)
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course Not found id:" + str(course_ident))
        grade.fk_course_id = course_ident
    db.add(grade)
    await db.commit()
    await db.refresh(grade)
    response.status_code = status.HTTP_201_CREATED
    return SchemaBaseGrade.model_validate(grade)


# -----------------------Update Routes------------------------
async def update_one(
        ident: UUID4,
        grade: Optional[float] = None,
        db=Depends(get_db)) -> SchemaBaseGrade:
    res = await db.get(DBGrade, ident)
    if not res:
        raise NOT_FOUND
    if grade is not None:
        res.grade = grade
    await db.commit()
    await db.refresh(res)
    return SchemaBaseGrade.model_validate(res)


# -----------------------Delete Routes------------------------
async def delete_one(ident: UUID4, db=Depends(get_db)):
    res = await db.get(DBGrade, ident)
    if not res:
        raise NOT_FOUND
    res.student = None
    res.course = None
    await db.commit()
    await db.delete(res)
    await db.commit()
    return {'message': 'Deleted', 'id': ident}


# ----------------------Relation Routes-----------------------
