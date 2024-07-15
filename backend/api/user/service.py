from http.client import HTTPException

from sqlalchemy import select
from sqlalchemy.orm import session

from api.user.schemas import AuthSchemaBase, AuthSchemaCreate
from common.security.jwt import get_hash_password
from core.db import async_db_session
from models.user import User


class UserService:
    @staticmethod
    async def registration(credentials: AuthSchemaBase) -> AuthSchemaCreate:
        user = await UserService().get_user_by_email(credentials.email)

        if user:
            raise HTTPException("User already exist")

        user = None
        async with async_db_session.begin() as db:
            password_hash = await get_hash_password(credentials.password)
            user = User(
                email=credentials.email,
                password=password_hash,
                username=credentials.username,
                refresh_token=None
            )
            db.add(user)
            await db.commit()
        return AuthSchemaCreate(
            id=user.id,
            email=user.email,
            username=user.username,
            password=user.password,
            created_at=user.created_time,
            updated_at=user.updated_time,
        )

    @staticmethod
    async def get_user_by_email(email: str) -> User | None:
        async with async_db_session.begin() as db:
            query = select(User).where(User.email == email)
            result = await db.execute(query)
            user = result.scalar()
            if user is None:
                return None
            return user
