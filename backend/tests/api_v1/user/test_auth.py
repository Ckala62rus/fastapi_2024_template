import httpx
import pytest
from fastapi.testclient import TestClient
from common.log import logger

from core.config import settings
from tests.conftest import app

# Run test
# pytest -v --pyargs tests
# pytest -v --pyargs tests --capture=no

@pytest.mark.asyncio
def test_registration_sync(
    app: TestClient,
) -> None:
    data = {
        "email": "2admin@mail.ru",
        "password": "123123",
        "username": "2admin"
    }
    response = app.post(f'{settings.API_V1_STR}/user/registration', json=data)
    logger.debug(response.json())
    assert response.status_code == 200
    assert response.json()['code'] == 201

def test_login(
    app: TestClient,
) -> None:
    registration_data = {
        "email": "2admin@mail.ru",
        "password": "123123",
        "username": "2admin"
    }
    client = app
    client.post(f'{settings.API_V1_STR}/user/registration', json=registration_data)
    response = client.post(f'{settings.API_V1_STR}/user/login', json={
        "email": registration_data['email'],
        "password": registration_data['password'],
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

def test_get_all_users(
    app: TestClient,
) -> None:
    registration_data = {
        "email": "2admin@mail.ru",
        "password": "123123",
        "username": "2admin"
    }
    client = app
    client.post(f'{settings.API_V1_STR}/user/registration', json=registration_data)

    auth = client.post(f'{settings.API_V1_STR}/user/login', json={
        "email": registration_data['email'],
        "password": registration_data['password'],
    })
    auth_token = auth.json()['data']['access_token']

    response_users = client.get(f'{settings.API_V1_STR}/user/users?page=1&limit=10',
        headers={
            'Authorization': f'Bearer {auth_token}'
        }
    )

    users_count = len(response_users.json()['data'])

    assert response_users.status_code == httpx.codes.OK
    assert users_count == 1
