# JWT authorizes dependency injection
import time
from datetime import datetime, timedelta
from typing import Dict

from fastapi.security.utils import get_authorization_scheme_param
from starlette.requests import Request

import jwt
from passlib.context import CryptContext

from fastapi import Depends
from fastapi.security import HTTPBearer

from common.exception.errors import TokenError
from core.config import settings
from core.db_redis import redis_client
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
    token_info["token_type"] = 'Bearer'
    token_info["user_id"] = user_id
    token_info["expires"] = timezone.datetime_to_format(timezone.now() + timedelta(seconds=settings.TOKEN_TIME_EXPIRES))

    return token_info


async def create_jwt_refresh_token(user_id: int) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + int(settings.TOKEN_REFRESH_EXPIRE_SECONDS)
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

    token_info = dict()
    token_info["refresh_token"] = token
    token_info["token_type"] = 'Bearer'
    token_info["user_id"] = user_id
    token_info["expires"] = timezone.datetime_to_format(timezone.now() + timedelta(seconds=settings.TOKEN_REFRESH_EXPIRE_SECONDS))

    return token_info


async def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        token_from_redis = redis_client.get(f'{settings.TOKEN_REDIS_PREFIX}:{decoded_token["user_id"]}:{token}')
        if token_from_redis is None:
            raise TokenError("Invalid authentication token")
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except Exception as e:
        return {}


async def decode_refresh_jwt(token: str) -> dict:
    """
    Decode refresh token without Redis validation
    
    :param token: The refresh token to decode
    :return: Decoded token payload or empty dict if invalid
    """
    try:
        decoded_token = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else {}
    except Exception as e:
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


async def create_access_token_redis(sub: str, expires_delta: timedelta | None = None, **kwargs) -> tuple[str, str]:
    """
    Generate encryption token

    :param sub: The subject/userid of the JWT
    :param expires_delta: Increased expiry time
    :return:
    """
    token_info = await sign_jwt(user_id=int(sub))
    key = f'{settings.TOKEN_REDIS_PREFIX}:{sub}:{token_info["access_token"]}'
    redis_client.setex(key, settings.TOKEN_TIME_EXPIRES, token_info["access_token"])
    return token_info["access_token"], token_info["expires"]


async def create_refresh_token_redis(
    sub: str,
    token: str | None = None,
    refresh_token: str | None = None
) -> tuple[str, str]:
    """
    Generate refresh token

    :param sub: The subject/userid of the JWT
    :param expire_time: expiry time
    :return:
    """
    token_info = await create_jwt_refresh_token(user_id=int(sub))

    if refresh_token is not None and token is not None:
        token_key = f'{settings.TOKEN_REDIS_PREFIX}:{sub}:{token}'
        refresh_token_key = f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{sub}:{refresh_token}'
        redis_client.delete(token_key)
        redis_client.delete(refresh_token_key)

    key = f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{sub}:{token_info["refresh_token"]}'
    redis_client.setex(key, settings.TOKEN_REFRESH_EXPIRE_SECONDS, token_info["refresh_token"])
    return token_info["refresh_token"], token_info["expires"]


async def create_new_token(sub: str, token: str, refresh_token: str, **kwargs) -> tuple[str, str, datetime, datetime]:
    """
    Generate new token

    :param sub:
    :param token
    :param refresh_token:
    :return:
    """
    redis_refresh_token = await redis_client.get(f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{sub}:{refresh_token}')
    if not redis_refresh_token or redis_refresh_token != refresh_token:
        raise TokenError(msg='Refresh Token error')
    new_access_token, new_access_token_expire_time = await create_access_token_redis(sub, **kwargs)
    new_refresh_token, new_refresh_token_expire_time = await create_refresh_token_redis(sub, **kwargs)
    token_key = f'{settings.TOKEN_REDIS_PREFIX}:{sub}:{token}'
    refresh_token_key = f'{settings.TOKEN_REDIS_PREFIX}:{sub}:{refresh_token}'
    await redis_client.delete(token_key)
    await redis_client.delete(refresh_token_key)
    return new_access_token, new_refresh_token, new_access_token_expire_time, new_refresh_token_expire_time


async def get_token(request: Request) -> str:
    """
    Get token for request header

    :return:
    """
    authorization = request.headers.get('Authorization')
    scheme, token = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != 'bearer':
        raise TokenError(msg='Token incorrect')
    return token
