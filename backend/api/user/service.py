from http.client import HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.user.schemas import (
    AuthSchemaBase,
    AuthSchemaCreatedNewUser,
    AuthLoginSchema,
    MeSchema
)
from common.security.jwt import get_hash_password, password_verify, sign_jwt
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
    ) -> dict[str, str]:
        user = await UserService.get_user_by_email(credentials.email, db)

        if user is None:
            raise HTTPException(f"User with email {credentials.email} not found")

        is_verify_password = await password_verify(credentials.password, user.password)
        if not is_verify_password:
            raise HTTPException("Incorrect password")

        return await sign_jwt(user.id)

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
