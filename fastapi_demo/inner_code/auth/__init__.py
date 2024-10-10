# generate_hash: 73a845301d8b23fa6e7061cdce90493e
"""
This file was automatically generated in 2024-10-10 15:04:55.316784
"""
import datetime
from typing import Optional
from sqlalchemy import select

from fastapi_toolkit.base.auth.key import AuthDBBackend as AuthDBBackendBase, Auth

from ..db import get_db_sync
from ..models import DBUser
from ..schemas import SchemaBaseUser


class AuthDBBackend(AuthDBBackendBase):
    def get_user(self, user_key: str) -> Optional[DBUser]:
        db = next(get_db_sync())
        user = db.execute(select(DBUser).where(DBUser.user_key.__eq__(user_key)).limit(1))
        return user.scalars().one_or_none()

    def add_user(self, create: SchemaBaseUser) -> DBUser:
        db = next(get_db_sync())
        user = DBUser(
            **create.model_dump(exclude={'id', 'created_at', 'updated_at', 'deleted_at'}),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def access(self, user_key: str) -> None:
        db = next(get_db_sync())
        user = self.get_user(user_key)
        user.accessed_at = datetime.datetime.now(datetime.UTC)
        db.commit()


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
