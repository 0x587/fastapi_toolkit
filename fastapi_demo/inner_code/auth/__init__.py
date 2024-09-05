# generate_hash: 1d2058c2879b4f494940ceb5356c692c
"""
This file was automatically generated in 2024-09-05 10:54:53.725977
"""
import datetime
from typing import Optional
from sqlalchemy import select

from fastapi_toolkit.base.auth.key import AuthDBBackend as AuthDBBackendBase, Auth

from ..db import sessionmanager
from ..models import DBUser
from ..schemas import SchemaBaseUser


class AuthDBBackend(AuthDBBackendBase):
    async def get_user(self, user_key: str) -> Optional[DBUser]:
        async with sessionmanager.session() as db:
            user = await db.execute(select(DBUser).where(DBUser.user_key.__eq__(user_key)).limit(1))
            return user.scalars().one_or_none()

    async def add_user(self, create: SchemaBaseUser) -> DBUser:
        async with sessionmanager.session() as db:
            user = DBUser(
                **create.model_dump(exclude={'id', 'created_at', 'updated_at', 'deleted_at'}),
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
            return user

    async def access(self, user_key: str) -> None:
        async with sessionmanager.session() as db:
            user = await self.get_user(user_key)
            user.accessed_at = datetime.datetime.now(datetime.UTC)
            await db.commit()


class AuthFactory:
    @classmethod
    def create(cls, key_name: str):
        db_backend = AuthDBBackend()
        return Auth(
            db_backend=db_backend,
            key_name=key_name,
            schema_user=SchemaBaseUser,
            schema_user_full=SchemaBaseUser,
        )


__all__ = [
    "AuthFactory",
]
