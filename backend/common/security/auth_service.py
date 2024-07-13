from typing import Tuple, Dict, Any, Coroutine

from common.security.jwt import (
    password_verify,
    get_hash_password,
    decode_jwt,
    sign_jwt
)

# todo Вынести логику в БД
user = {
    'id': 1,
    'name': 'admin',
    'email': 'admin@mail.ru',
    'password': '$2b$12$MbK8SYyRisQUxQaR9eXMe.kVe/52sN2ecA62hFZpUvYbk5L.R2nJG',
}

# todo Скорее чвсего тут не место этому сервису.Нужно создать отдельное приложения
class AuthService:
    @staticmethod
    async def login(
        *,
        login: str,
        password: str,
    ) -> Dict[str, str] | None:
        user_from_database = user
        # hash_password = await get_hash_password(password)
        is_verify_password = await password_verify(password, user_from_database['password'])

        if is_verify_password:
            token = await sign_jwt(user_from_database['id'])
            return token

        return None


auth_service = AuthService()
