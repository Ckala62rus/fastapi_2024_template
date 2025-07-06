from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette.requests import Request

from api.user.schemas import (
    AuthSchemaBase,
    AuthSchemaCreatedNewUser,
    AuthLoginSchema,
    MeSchema,
    GetLoginToken,
    GetNewToken
)
from common.security.jwt import (
    get_hash_password,
    password_verify,
    create_access_token_redis,
    create_refresh_token_redis,
    get_token,
    decode_jwt,
    decode_refresh_jwt
)
from common.exception.errors import TokenError
from core.config import settings
from core.db_redis import redis_client
from models.user import User


class UserService:
    @staticmethod
    async def registration(
            credentials: AuthSchemaBase,
            db: AsyncSession
    ) -> AuthSchemaCreatedNewUser:
        user = await UserService().get_user_by_email(credentials.email, db)

        if user:
            raise HTTPException(status_code=400, detail="User already exist")

        user = None
        password_hash = await get_hash_password(credentials.password)
        user = User(
            email=credentials.email,
            password=password_hash,
            username=credentials.username,
            refresh_token=None
        )
        db.add(user)
        await db.commit()
        return AuthSchemaCreatedNewUser(
            id=user.id,
            email=user.email,
            username=user.username,
            created_time=user.created_time,
            updated_time=user.updated_time,
        )

    @staticmethod
    async def get_user_by_email(
            email: str,
            db: AsyncSession
    ) -> User | None:
        query = select(User).where(User.email == email)
        result = await db.execute(query)
        user = result.scalar()
        if user is None:
            return None
        return user

    @staticmethod
    async def get_all_users(
            db: AsyncSession,
            limit: int = 10,
            page: int = 1,
    ):
        skip = (page - 1) * limit
        query = (
            select(User)
            .order_by(User.id.desc())
            .options(selectinload(User.permissions))
        ).limit(limit).offset(skip)
        result = await db.execute(query)
        users = result.scalars().all()
        return users

    @staticmethod
    async def login(
            credentials: AuthLoginSchema,
            db: AsyncSession
    ) -> GetLoginToken:
        user = await UserService.get_user_by_email(credentials.email, db)

        if user is None:
            raise HTTPException(status_code=400, detail=f"User with email {credentials.email} not found")

        is_verify_password = await password_verify(credentials.password, user.password)
        if not is_verify_password:
            raise HTTPException(status_code=400, detail="Incorrect password")

        access_token, access_token_expire_time = await create_access_token_redis(str(user.id))
        refresh_token, refresh_token_expire_time = await create_refresh_token_redis(str(user.id))
        # todo await user_dao.update_login_time(db, obj.username) need create method for last login
        # todo await db.refresh(current_user)
        return GetLoginToken(
            access_token=access_token,
            refresh_token=refresh_token,
            access_token_expire_time=access_token_expire_time,
            refresh_token_expire_time=refresh_token_expire_time,
        )

    @staticmethod
    async def logout(*, request: Request) -> None:
        prefix = f'{settings.TOKEN_REDIS_PREFIX}:{request.state.user_id}:'
        refresh_tokens = f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{request.state.user_id}:*'
        await redis_client.delete_prefix(prefix)
        for key in redis_client.scan_iter(refresh_tokens):
            redis_client.delete(key)

    @staticmethod
    async def get_user_by_id(
            user_id: int,
            db: AsyncSession
    ) -> User | None:
        query = (
            select(User)
            .where(User.id == user_id).
            options(selectinload(User.permissions))
        )
        result = await db.execute(query)
        user = result.scalar()
        if user is None:
            return None
        return user

    @staticmethod
    async def me(user_id: int, db: AsyncSession) -> MeSchema:
        user = await UserService.get_user_by_id(user_id, db)
        if user is None:
            raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
        return MeSchema(**user.__dict__)

# todo сделать отмену обычного токена и переделать логику.
# рефреш токен не меняется до тех пор пока не протухнет!
    @staticmethod
    async def token_refresh(
            *,
            request: Request,
            refresh_token: str,
            db: AsyncSession
    ) -> GetNewToken:
        # Валидация refresh токена
        try:
            # Декодируем refresh токен
            decoded_refresh = await decode_refresh_jwt(refresh_token)
            if not decoded_refresh:
                raise HTTPException(status_code=400, detail="Invalid or expired refresh token")
            
            # Получаем user_id из refresh токена
            refresh_user_id = decoded_refresh.get("user_id")
            if not refresh_user_id:
                raise HTTPException(status_code=400, detail="Invalid refresh token structure")
            
            # Проверяем что токен есть в Redis
            redis_refresh_key = f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{refresh_user_id}:{refresh_token}'
            redis_refresh_token = redis_client.get(redis_refresh_key)
            if not redis_refresh_token or redis_refresh_token != refresh_token:
                raise HTTPException(status_code=400, detail="Refresh token not found or invalid")
                
        except TokenError:
            raise HTTPException(status_code=400, detail="Invalid refresh token")
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid refresh token")
        
        user = await UserService.get_user_by_id(request.state.user_id, db)
        if user is None:
            raise HTTPException(status_code=404, detail=f"User with id {request.state.user_id} not found")
            
        old_token = await get_token(request)
        
        # Создаем новые токены только после успешной валидации
        new_access_token, new_access_token_expire_time = await create_access_token_redis(str(user.id))
        new_refresh_token, new_refresh_token_expire_time = await create_refresh_token_redis(
            str(user.id),
            old_token,
            refresh_token
        )
        
        data = GetNewToken(
            access_token=new_access_token,
            access_token_expire_time=new_access_token_expire_time,
            refresh_token=new_refresh_token,
            refresh_token_expire_time=new_refresh_token_expire_time,
        )
        return data


user_service = UserService()
