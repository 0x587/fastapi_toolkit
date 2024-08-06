# generate_hash: a7414d32bb0ada92e68f58a6707ce2a1
"""
This file was automatically generated in 2024-08-06 22:49:59.084445
"""

import asyncio
import random
from typing import Callable

from .auth.models import DBUser
from .auth import AuthFactory
from .models import *
from .db import sessionmanager
from polyfactory import PostGenerated
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory

from .setting import get_settings
setting = get_settings()
SECRET_KEY = setting.secret_key
ALGORITHM = setting.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = setting.access_token_expire_minutes
auth = AuthFactory.create(SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES)

class UserFactory(SQLAlchemyFactory[DBUser]):
    __sync_persistence__ = True

    scopes = ''

    @staticmethod
    def _username() -> Callable[..., str]:
        flag = -1

        def f(*args, **kwargs):
            nonlocal flag
            flag += 1
            return 'admin' if flag == 0 else f'user{flag}'

        return f

    username = PostGenerated(_username())

    @staticmethod
    def _hashed_password() -> Callable[..., str]:
        flag = -1

        def f(*args, **kwargs):
            nonlocal flag
            flag += 1
            return auth.get_password_hash('admin' if flag == 0 else f'user{flag}')

        return f

    hashed_password = PostGenerated(_hashed_password())

    @staticmethod
    def _is_superuser() -> Callable[..., bool]:
        flag = -1

        def f(*args, **kwargs):
            nonlocal flag
            flag += 1
            return flag == 0

        return f

    is_superuser = PostGenerated(_is_superuser())

    @staticmethod
    def _is_active() -> Callable[..., bool]:
        flag = -1

        def f(*args, **kwargs):
            nonlocal flag
            flag += 1
            return True if flag == 0 else random.choice([True, False])

        return f

    is_active = PostGenerated(_is_active())

    @classmethod
    def registered_at(cls):
        return datetime.datetime.utcnow()

    @staticmethod
    def _activated_at(name: str, values: dict, *args, **kwargs) -> datetime:
        if values['is_active']:
            return datetime.datetime.utcnow()
        return None

    activated_at = PostGenerated(_activated_at)
    last_login_at = None
    accessed_at = None


class DepartmentFactory(SQLAlchemyFactory[DBDepartment]):
    __sync_persistence__ = True



class StudentFactory(SQLAlchemyFactory[DBStudent]):
    __sync_persistence__ = True



class CourseFactory(SQLAlchemyFactory[DBCourse]):
    __sync_persistence__ = True
    __set_relationships__ = True

    @classmethod
    def grades(cls):
        return [GradeFactory.build() for _ in range(10)]

    @classmethod
    def teachers(cls):
        return [TeacherFactory.build() for _ in range(10)]



class TeacherFactory(SQLAlchemyFactory[DBTeacher]):
    __sync_persistence__ = True



class GradeFactory(SQLAlchemyFactory[DBGrade]):
    __sync_persistence__ = True
    __set_relationships__ = True

    @classmethod
    def student(cls):
        return StudentFactory.build()

    @classmethod
    def course(cls):
        return None



def main():
    async def f():
        async with sessionmanager.session() as session:
            UserFactory.__async_session__ = session
            DepartmentFactory.__async_session__ = session
            StudentFactory.__async_session__ = session
            CourseFactory.__async_session__ = session
            TeacherFactory.__async_session__ = session
            GradeFactory.__async_session__ = session

            await CourseFactory.create_batch_async(size=10)
            await UserFactory.create_batch_async(size=10)
            await DepartmentFactory.create_batch_async(size=10)

    asyncio.run(f())
