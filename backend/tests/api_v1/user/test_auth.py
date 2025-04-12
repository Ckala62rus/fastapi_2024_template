import logging

import httpx
import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from fastapi.testclient import TestClient
import logging

from core.config import settings
from tests.conftest import app, PYTEST_EMAIL, PYTEST_USERNAME

logger  = logging.getLogger(__name__)
logger.info("Logging test info message****************")
logger.debug("Logging test debug message****************")

# Run test
# pytest -v --pyargs tests
# pytest -v --pyargs tests --capture=no


# @pytest.mark.asyncio
# async def test_me(
#     # client: TestClient,
#     token_headers: dict[str, str]
# ) -> None:
#     async with AsyncClient(
#         transport=ASGITransport(app=app), base_url="http://test"
#     ) as async_client:
#         response = await async_client.get(f'{settings.API_V1_STR}/user/me', headers= token_headers)
#     assert response.status_code == 200
#     assert response.json()['code'] == 200
#     assert response.json()['data']['email'] == PYTEST_EMAIL
#     assert response.json()['data']['username'] == PYTEST_USERNAME

# @pytest.mark.asyncio
# async def test_registration(
#     # async_client: AsyncClient
#         app: FastAPI,
#         log: logging.Logger
# ) -> None:
#     data = {
#         "email": "2admin@mail.ru",
#         "password": "123123",
#         "username": "2admin"
#     }
#     assert True == True
#
#     log.info('Logging test info message')
#     async with AsyncClient(
#             transport=ASGITransport(app=app), base_url="http://test"
#     ) as async_client:
#         response = await async_client.post(f'{settings.API_V1_STR}/user/registration', json=data)
#         log.info(response)
#     # response = await async_client.post(f'{settings.API_V1_STR}/user/registration', json=data)
#     assert response.status_code == 200
#     print(response.status_code)
#     logger.info("++++++++++++++++++++++++++++++++++++++")


def test_registration_sync(
    app: FastAPI,
    # log: logging.Logger
) -> None:
    data = {
        "email": "2admin@mail.ru",
        "password": "123123",
        "username": "2admin"
    }
    client = TestClient(app)
    response = client.post(f'{settings.API_V1_STR}/user/registration', json=data)

    assert response.status_code == 200
    assert response.json()['code'] == 201

def test_login(
    app: FastAPI,
    # log: logging.Logger
) -> None:
    registration_data = {
        "email": "2admin@mail.ru",
        "password": "123123",
        "username": "2admin"
    }
    client = TestClient(app)
    client.post(f'{settings.API_V1_STR}/user/registration', json=registration_data)
    response = client.post(f'{settings.API_V1_STR}/user/login', json={
        "email": registration_data['email'],
        "password": registration_data['password'],
        # "password": 'qwerty',
    })

    result = response.json()

    assert response.status_code == 200
    assert len(result['data']['access_token']) > 0

def test_me(
    app: FastAPI,
) -> None:
    registration_data = {
        "email": "2admin@mail.ru",
        "password": "123123",
        "username": "2admin"
    }
    client = TestClient(app)
    client.post(f'{settings.API_V1_STR}/user/registration', json=registration_data)
    auth = client.post(f'{settings.API_V1_STR}/user/login', json={
        "email": registration_data['email'],
        "password": registration_data['password'],
    })

    auth_token = auth.json()['data']['access_token']

    response = client.get(f'{settings.API_V1_STR}/user/me',
        headers={
            'Authorization': f'Bearer {auth_token}'
        }
    )
    result = response.json()

    assert response.status_code == httpx.codes.OK
    assert result["data"]["email"] == registration_data["email"]
