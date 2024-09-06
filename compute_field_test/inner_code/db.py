# generate_hash: 69ed5fd22e60802878d4f0ff103c97c4
"""
This file was automatically generated in 2024-09-06 16:25:32.742037
"""
from typing import Any, AsyncIterator, Annotated, Generator
import contextlib

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection, AsyncSession, async_sessionmaker, AsyncAttrs
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from .setting import get_settings

setting = get_settings()
username = setting.username
password = setting.password
host = setting.host
db_name = setting.database

database_url = f"mysql+aiomysql://{username}:{password}@{host}/{db_name}"

async_engine = create_async_engine(database_url)
sync_engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}/{db_name}")


class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any] = {}):
        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(database_url)


async def get_db_session():
    async with sessionmanager.session() as session:
        yield session


DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]


async def get_db() -> AsyncSession:
    async_session = async_sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


def get_db_sync() -> Generator[Session, Any, None]:
    session = sessionmaker(sync_engine, class_=Session, expire_on_commit=False)
    with session() as session:
        yield session


class Base(AsyncAttrs, DeclarativeBase):
    pass