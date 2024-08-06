# generate_hash: 4dbb20d1d72d4bf365bf25df6f2cbcbb
"""
This file was automatically generated in 2024-08-06 22:49:59.076139
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
async def get_one(ident: UUID4, db=Depends(get_db)) -> SchemaBaseDepartment:
    res = await db.get(DBDepartment, ident)
    if res:
        return res
    raise NOT_FOUND


async def __get_all_query(
        filter_name: Optional[str] = None,
        sort_by: Optional[str] = None, is_desc: bool = False,
) -> Select:
    query = select(DBDepartment)
    if filter_name is not None:
        query = query.filter(DBDepartment.name == filter_name)
    if sort_by is not None:
        if is_desc:
            query = query.order_by(getattr(DBDepartment, sort_by).desc())
        else:
            query = query.order_by(getattr(DBDepartment, sort_by))
    return query


async def get_all(
        query=Depends(__get_all_query),
        db=Depends(get_db)
) -> Page[SchemaBaseDepartment]:
    return await paginate(db, query)


async def get_link_all(
        query=Depends(__get_all_query),
        db=Depends(get_db)
) -> Page[SchemaDepartment]:
    return await paginate(db, query)
# ---------------------User Query Routes----------------------


# -----------------------Create Routes------------------------
async def create_one(
        name: str,
        response: Response, db=Depends(get_db)
) -> SchemaBaseDepartment:
    department = SchemaBaseDepartment(
        name=name,
    )
    department = DBDepartment(**department.model_dump())
    db.add(department)
    await db.commit()
    await db.refresh(department)
    response.status_code = status.HTTP_201_CREATED
    return SchemaBaseDepartment.model_validate(department)


# -----------------------Update Routes------------------------
async def update_one(
        ident: UUID4,
        name: Optional[str] = None,
        db=Depends(get_db)) -> SchemaBaseDepartment:
    res = await db.get(DBDepartment, ident)
    if not res:
        raise NOT_FOUND
    if name is not None:
        res.name = name
    await db.commit()
    await db.refresh(res)
    return SchemaBaseDepartment.model_validate(res)


# -----------------------Delete Routes------------------------
async def delete_one(ident: UUID4, db=Depends(get_db)):
    res = await db.get(DBDepartment, ident)
    if not res:
        raise NOT_FOUND
    await db.delete(res)
    await db.commit()
    return {'message': 'Deleted', 'id': ident}


# ----------------------Relation Routes-----------------------
