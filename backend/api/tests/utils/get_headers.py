from httpx import AsyncClient
from starlette.testclient import TestClient

from core.config import settings


def get_token_headers(client: AsyncClient, email: str, password: str) -> dict[str, str]:
    data = {
        'email': email,
        'password': password,
    }
    response = client.post(f'{settings.API_V1_STR}/user/login', json=data)

    response.raise_for_status()

    token_type = response.json()['data']['token_type']
    access_token = response.json()['data']['access_token']
    headers = {'Authorization': f'{token_type} {access_token}'}
    return headers
