from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.db import create_engine_and_session

TEST_SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/test_db'

_, test_async_db_session = create_engine_and_session(TEST_SQLALCHEMY_DATABASE_URL)


async def override_get_db() -> AsyncSession:
    """session генератор"""
    session = test_async_db_session()
    try:
        yield session
    except Exception as se:
        await session.rollback()
        raise se
    finally:
        await session.close()
