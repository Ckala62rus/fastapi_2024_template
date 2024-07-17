import asyncio
import os
from typing import Generator, Dict, AsyncGenerator

import pytest
from starlette.testclient import TestClient
from httpx import AsyncClient

from api.tests.utils.db_postgres import override_get_db
from api.tests.utils.get_headers import get_token_headers
from core.db import get_db
from main import app

app.dependency_overrides[get_db] = override_get_db

# Test user
PYTEST_EMAIL = 'admin@mail.ru'
PYTEST_PASSWORD = '123123'
PYTEST_USERNAME = 'admin'

CLEAN_TABLES = [
    "users",
]


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True, scope='session')
def run_migrations() -> None:
    print('///////////////////////////////////////////////')
    # os.system("alembic init migrations")
    # os.system("alembic revision --autogenerate -m 'test running migrations'")
    # os.system("alembic upgrade heads")


@pytest.fixture(scope='session')
async def async_session_test():
    async_session = override_get_db()
    yield async_session


@pytest.fixture(scope='module')
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio(scope='function', autouse=True)
def clean_tables(async_session_test):
    """Clean data in all tables before running test function"""
    with async_session_test as session:
        with session.begin():
            for table_for_clearing in CLEAN_TABLES:
                session.execute(f"""TRUNCATE TABLE {table_for_clearing};""")


@pytest.fixture(scope='module')
def token_headers(client: TestClient) -> Dict[str, str]:
    return get_token_headers(client=client, email=PYTEST_EMAIL, password=PYTEST_PASSWORD)
