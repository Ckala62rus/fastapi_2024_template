from http.client import HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from api.user.schemas import (
    AuthSchemaBase,
    AuthSchemaCreatedNewUser,
    AuthLoginSchema,
    MeSchema, GetLoginToken
)
from common.security.jwt import (
    get_hash_password,
    password_verify,
    create_access_token_redis,
    create_refresh_token_redis, get_token
)
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
            raise HTTPException("User already exist")

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
            created_at=user.created_time,
            updated_at=user.updated_time,
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
    async def login(
            credentials: AuthLoginSchema,
            db: AsyncSession
    ) -> GetLoginToken:
        user = await UserService.get_user_by_email(credentials.email, db)

        if user is None:
            raise HTTPException(f"User with email {credentials.email} not found")

        is_verify_password = await password_verify(credentials.password, user.password)
        if not is_verify_password:
            raise HTTPException("Incorrect password")

        access_token, access_token_expire_time = await create_access_token_redis(str(user.id))
        # refresh_token, refresh_token_expire_time = await create_refresh_token_redis(
        #     str(user.id), access_token_expire_time
        # )
        # todo await user_dao.update_login_time(db, obj.username) need create method for last login
        # todo await db.refresh(current_user)
        data = GetLoginToken(
            access_token=access_token,
            # refresh_token=refresh_token,
            access_token_expire_time=access_token_expire_time,
            # refresh_token_expire_time=refresh_token_expire_time,
        )

        return data
        # return await sign_jwt(user.id)

    @staticmethod
    async def logout(*, request: Request) -> None:
        prefix = f'{settings.TOKEN_REDIS_PREFIX}:{request.user_id}:'
        await redis_client.delete_prefix(prefix)

    @staticmethod
    async def get_user_by_id(
            user_id: int,
            db: AsyncSession
    ) -> User | None:
        query = select(User).where(User.id == user_id)
        result = await db.execute(query)
        user = result.scalar()
        if user is None:
            return None
        return user

    @staticmethod
    async def me(user_id: int, db: AsyncSession) -> MeSchema:
        user = await UserService.get_user_by_id(user_id, db)
        if user is None:
            raise HTTPException(f"User with id {user_id} not found")
        return MeSchema(**user.__dict__)


user_service = UserService()
