# generate_hash: 3d96311f2a185c66ddefd33ead3348c5
"""
This file was automatically generated in 2024-08-06 22:49:59.085011
"""
import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy import select

from fastapi_toolkit.base.auth import AuthDBBackend as AuthDBBackendBase, Auth

from .models import DBUser, SchemaUserCreate, SchemaUser, SchemaUserFull
from ..db import sessionmanager


class AuthDBBackend(AuthDBBackendBase):
    async def get_user(self, username: str) -> Optional[DBUser]:
        async with sessionmanager.session() as db:
            user = await db.execute(select(DBUser).where(DBUser.username == username).limit(1))
            return user.scalars().one_or_none()

    async def add_user(self, create: SchemaUserCreate, hashed_password: str) -> DBUser:
        async with sessionmanager.session() as db:
            user = DBUser(**create.model_dump(exclude={'password'}),
                          id=uuid.uuid4(),
                          hashed_password=hashed_password,
                          registered_at=datetime.utcnow(),
                          )
            db.add(user)
            await db.commit()
            await db.refresh(user)
            return user

    async def access(self, username: str) -> None:
        async with sessionmanager.session() as db:
            user = await self.get_user(username)
            user.accessed_at = datetime.utcnow()
            await db.commit()


class AuthFactory:
    @classmethod
    def create(cls, secret_key, algorithm, access_token_expire_minutes):
        db_backend = AuthDBBackend()
        return Auth(
            secret_key=secret_key,
            algorithm=algorithm,
            access_token_expire_minutes=access_token_expire_minutes,
            db_backend=db_backend,
            SchemaUser=SchemaUser,
            SchemaUserFull=SchemaUserFull,
        )


__all__ = [
    "AuthFactory",
]
