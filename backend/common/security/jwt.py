# JWT authorizes dependency injection
import time
from datetime import datetime, timedelta
from typing import Dict

import jwt
from passlib.context import CryptContext

from fastapi import Depends
from fastapi.security import HTTPBearer

from core.config import settings
from utils.timezone import timezone

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

DependsJwtAuth = Depends(HTTPBearer())


async def sign_jwt(user_id: int) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + int(settings.TOKEN_TIME_EXPIRES)
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

    token_info = dict()
    token_info["access_token"] = token
    token_info["user_id"] = user_id
    token_info["expires"] = timezone.datetime_to_format(timezone.now() + timedelta(seconds=settings.TOKEN_TIME_EXPIRES))

    return token_info


async def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}


async def get_hash_password(password: str) -> str:
    """
    Encrypt passwords using the hash algorithm

    :param password:
    :return:
    """
    return pwd_context.hash(password)


async def password_verify(plain_password: str, hashed_password: str) -> bool:
    """
    Password verification

    :param plain_password: The password to verify
    :param hashed_password: The hash ciphers to compare
    :return:
    """
    return pwd_context.verify(plain_password, hashed_password)

