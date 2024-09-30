import datetime
from typing import Optional
from sqlalchemy import select

from fastapi_toolkit.base.auth.key import AuthDBBackend as AuthDBBackendBase, Auth

from ..db import get_db_sync
from ..models import DBUser
from ..schemas import SchemaBaseUser


class AuthDBBackend(AuthDBBackendBase):
    def get_user(self, user_key: str) -> Optional[DBUser]:
        with get_db_sync() as db:
            user = db.execute(select(DBUser).where(DBUser.user_key.__eq__(user_key)).limit(1))
            return user.scalars().one_or_none()


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
