from typing import Dict

import pytest_asyncio

from tests.utils.get_headers import get_token_headers

PYTEST_EMAIL = 'admin@mail.ru'
PYTEST_PASSWORD = '123123'
PYTEST_USERNAME = 'admin'
#
# CLEAN_TABLES = [
#     "users",
# ]
#
#
# @pytest.fixture(scope='session')
# def event_loop():
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()
#
#
# @pytest.fixture(autouse=True, scope='session')
# def run_migrations() -> None:
#     print('///////////////////////////////////////////////')
#     # os.system("alembic init migrations")
#     os.system("alembic revision --autogenerate -m 'test running migrations'")
#     os.system("alembic upgrade heads")
#
#
# @pytest.fixture(scope='session')
# async def async_session_test():
#     async_session = override_get_db()
#     yield async_session
#
#
# @pytest.fixture(scope='module')
# def client() -> Generator:
#     with TestClient(app) as c:
#         yield c
#
#
# @pytest.fixture(scope="session")
# async def ac() -> AsyncGenerator[AsyncClient, None]:
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         yield ac
#
#
# @pytest.mark.asyncio(scope='function', autouse=True)
# def clean_tables(async_session_test):
#     """Clean data in all tables before running test function"""
#     with async_session_test as session:
#         with session.begin():
#             for table_for_clearing in CLEAN_TABLES:
#                 session.execute(f"""TRUNCATE TABLE {table_for_clearing};""")
#
#
import os
import warnings

import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager
from databases import Database

import alembic
from alembic.config import Config
from alembic import command
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_db


import logging

logging.basicConfig(level=logging.DEBUG)
logger  = logging.getLogger(__name__)
logger.info("Logging test info message")
logger.debug("Logging test debug message")


# Apply migrations at beginning and end of testing session
@pytest_asyncio.fixture(scope="session")
def apply_migrations():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    os.environ["TESTING"] = "1"
    config = Config("alembic.ini")

    # logger.info(config)

    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")


# Create a new application for testing
@pytest_asyncio.fixture
def app(apply_migrations: None) -> FastAPI:
    from core.register import register_app

    return register_app()


# Grab a reference to our database when needed
@pytest_asyncio.fixture
def db(app: FastAPI) -> AsyncSession:
    return get_db()

@pytest_asyncio.fixture
def log() -> logging.Logger:
    return logger


@pytest_asyncio.fixture(scope='session')
async def async_client() -> AsyncClient:
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as async_client:
        return async_client

# @pytest_asyncio.fixture()
# async def token_headers(async_client: AsyncClient) -> Dict[str, str]:
#     return await get_token_headers(client=async_client, email=PYTEST_EMAIL, password=PYTEST_PASSWORD)


# @pytest.fixture
# async def test_cleaning(db: Database) -> CleaningInDB:
#     cleaning_repo = CleaningsRepository(db)
#     new_cleaning = CleaningCreate(
#         name="fake cleaning name", description="fake cleaning description", price=9.99, cleaning_type="spot_clean",
#     )
#
#     return await cleaning_repo.create_cleaning(new_cleaning=new_cleaning)


# Make requests in our tests
# @pytest.fixture
# async def client(app: FastAPI) -> AsyncClient:
#     async with LifespanManager(app):
#         async with AsyncClient(
#             app=app, base_url="http://testserver", headers={"Content-Type": "application/json"}
#         ) as client:
#             yield client

# @pytest_asyncio.fixture(scope='session')
# async def async_client() -> AsyncClient:
#     return AsyncClient(app=app, base_url='http://testserver')
