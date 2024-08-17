# generate_hash: 8432051ae57ec2c50c2b415032b640c0
"""
This file was automatically generated in 2024-08-18 00:30:05.042152
"""

from typing import List, Optional
from fastapi import Depends, Response, HTTPException, status
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
async def get_one(ident: int, db=Depends(get_db)) -> SchemaBaseGroup:
    res = await db.get(DBGroup, ident)
    if res and res.deleted_at is None:
        return res
    raise NOT_FOUND


async def batch_get(idents: List[int], db=Depends(get_db)) -> Page[SchemaBaseGroup]:
    query = select(DBGroup).filter(DBGroup.deleted_at.is_(None)).filter(DBGroup.id.in_(idents))
    return await paginate(db, query)


async def get_all_query(
        filter_name: Optional[str] = None,
        sort_by: Optional[str] = None, is_desc: bool = False,
) -> Select:
    query = select(DBGroup).filter(DBGroup.deleted_at.is_(None))
    if filter_name is not None:
        query = query.filter(DBGroup.name.__eq__(filter_name))
    if sort_by is not None:
        if is_desc:
            query = query.order_by(getattr(DBGroup, sort_by).desc())
        else:
            query = query.order_by(getattr(DBGroup, sort_by))
    return query


async def get_all(
        query=Depends(get_all_query),
        db=Depends(get_db)
) -> Page[SchemaBaseGroup]:
    return await paginate(db, query)


async def get_link_all(
        query=Depends(get_all_query),
        db=Depends(get_db)
) -> Page[SchemaGroup]:
    return await paginate(db, query)
# ---------------------User Query Routes----------------------


# -----------------------Create Routes------------------------
async def create_one(
        name: str,
        db=Depends(get_db)
) -> SchemaBaseGroup:
    group = SchemaBaseGroup(
        name=name,
    )
    group = DBGroup(**group.model_dump())
    db.add(group)
    await db.commit()
    await db.refresh(group)
    return SchemaBaseGroup.model_validate(group)


# -----------------------Update Routes------------------------
async def update_one(
        ident: int,
        name: Optional[str] = None,
        db=Depends(get_db)) -> SchemaBaseGroup:
    res = await db.get(DBGroup, ident)
    if not res or res.deleted_at is not None:
        raise NOT_FOUND
    if name is not None:
        res.name = name
    res.updated_at = datetime.datetime.now()
    await db.commit()
    await db.refresh(res)
    return SchemaBaseGroup.model_validate(res)


# -----------------------Delete Routes------------------------
async def delete_one(ident: int, db=Depends(get_db)):
    res = await db.get(DBGroup, ident)
    if not res or res.deleted_at is not None:
        raise NOT_FOUND
# TODO
    res.deleted_at = datetime.datetime.now()
    await db.commit()
    return {'message': 'Deleted', 'id': ident}


# ----------------------Relation Routes-----------------------


async def get_users_id_is(user_id: int, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaGroup]:
    if type(query) is not Select:
        query = await get_all_query()
    query = query.join(DBUser).filter(DBUser.id.__eq__(user_id))
    query = query.options(selectinload(DBGroup.users))
    return (await db.scalars(query)).all()
                

async def get_users_is(user: SchemaBaseUser, db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaGroup]:
    if type(query) is not Select:
        query = await get_all_query()
    query = query.join(DBUser).filter(DBUser.id.__eq__(user.id))
    query = query.options(selectinload(DBGroup.users))
    return (await db.scalars(query)).all()
                

async def get_users_id_has(user_ids: List[int], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaGroup]:
    if type(query) is not Select:
        query = await get_all_query()
    query = query.join(DBUser).filter(DBUser.id.in_(user_ids))
    query = query.options(selectinload(DBGroup.users))
    return (await db.scalars(query)).all()
                

async def get_users_has(users: List[SchemaBaseUser], db=Depends(get_db), query=Depends(get_all_query)) -> List[SchemaGroup]:
    if type(query) is not Select:
        query = await get_all_query()
    query = query.join(DBUser).filter(DBUser.id.in_(map(lambda x: x.id, users)))
    query = query.options(selectinload(DBGroup.users))
    return (await db.scalars(query)).all()
                
