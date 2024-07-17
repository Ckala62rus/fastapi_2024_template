from starlette.testclient import TestClient

from api.tests.conftest import PYTEST_EMAIL, PYTEST_USERNAME
from core.config import settings


def test_me(
    client: TestClient,
    token_headers: dict[str, str]
) -> None:
    response = client.get(f'{settings.API_V1_STR}/user/me', headers=token_headers)
    assert response.status_code == 200
    assert response.json()['code'] == 200
    assert response.json()['data']['email'] == PYTEST_EMAIL
    assert response.json()['data']['username'] == PYTEST_USERNAME


def test_registration(
    client: TestClient,
) -> None:
    data = {
        "email": "2admin@mail.ru",
        "password": "123123",
        "username": "2admin"
    }
    response = client.post(f'{settings.API_V1_STR}/user/registration', json=data)
    assert response.status_code == 200
    print('******************************')
    print(response.json()['data'])
    print('******************************')
