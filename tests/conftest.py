import pytest_asyncio
from app import repository, database


@pytest_asyncio.fixture
async def sqlite_db():
    db = database.AsyncDatabase("sqlite+aiosqlite:///test.sqlite")
    await db.drop_database()
    await db.create_database()
    yield db


@pytest_asyncio.fixture
async def repo(sqlite_db):
    yield repository.AsyncUserRepository(sqlite_db)
