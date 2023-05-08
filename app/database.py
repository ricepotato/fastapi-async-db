import logging
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

log = logging.getLogger(__name__)


class Base(DeclarativeBase):
    pass


class AsyncDatabase:
    def __init__(self, db_url: str) -> None:
        self._engine = create_async_engine(db_url, echo=False)
        self._async_session_factory = async_sessionmaker(
            self._engine, expire_on_commit=False
        )

    async def create_database(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_database(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    @asynccontextmanager
    async def session(self):
        async with self._async_session_factory() as session:
            try:
                yield session
            except Exception:
                log.exception("Session rollback because of exception")
                await session.rollback()
                raise
            finally:
                await session.close()

    async def close(self) -> None:
        await self._engine.dispose()
