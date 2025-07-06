from datetime import datetime
from typing import Annotated

from pydantic import EmailStr, Field, validator

from common.schema import SchemaBase


class AuthSchemaBase(SchemaBase):
    """🔐 Базовая схема авторизации для регистрации пользователей"""
    email: EmailStr
    password: Annotated[str, Field(min_length=6, max_length=50)]
    username: Annotated[str, Field(min_length=2, max_length=20, pattern=r'^[a-zA-Z0-9_.-]+$')]

    @validator('password')
    def validate_password(cls, v):
        if not v or v.isspace():
            raise ValueError('Password cannot be empty or contain only spaces')
        return v

    @validator('username')
    def validate_username(cls, v):
        if not v or v.isspace():
            raise ValueError('Username cannot be empty or contain only spaces')
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "john.doe@company.com",
                    "password": "MySecretPassword123",
                    "username": "john_doe"
                },
                {
                    "email": "admin@example.com", 
                    "password": "AdminPassword2024",
                    "username": "admin_user"
                }
            ]
        }
    }


class AccessTokenBase(SchemaBase):
    """🎫 Базовая схема токена доступа"""
    access_token: str
    access_token_type: str = 'Bearer'
    access_token_expire_time: datetime


class GetLoginToken(AccessTokenBase):
    """🔄 Схема токенов при входе в систему"""
    refresh_token: str
    refresh_token_type: str = 'Bearer'
    refresh_token_expire_time: datetime


class GetNewToken(AccessTokenBase):
    """🆕 Схема обновленных токенов"""
    refresh_token: str
    refresh_token_type: str = 'Bearer'
    refresh_token_expire_time: datetime


class AuthSchemaCreate(AuthSchemaBase):
    """✅ Схема созданного пользователя"""
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None


class AuthSchemaCreatedNewUser(SchemaBase):
    """🎉 Схема нового зарегистрированного пользователя"""
    id: int
    email: EmailStr
    username: str
    created_time: datetime | None = None
    updated_time: datetime | None = None


class AuthLoginSchema(SchemaBase):
    """🔐 Схема для входа в систему"""
    email: EmailStr
    password: Annotated[str, Field(min_length=6, max_length=50)]

    @validator('password')
    def validate_password(cls, v):
        if not v or v.isspace():
            raise ValueError('Password cannot be empty or contain only spaces')
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "john.doe@company.com",
                    "password": "MyPassword123",
                },
                {
                    "email": "admin@example.com",
                    "password": "AdminPassword2024",
                }
            ]
        }
    }


class MeSchema(AuthSchemaCreatedNewUser):
    """👤 Схема профиля пользователя с ролями"""
    is_superuser: bool
    is_staff: bool

    # Для того, что бы можно было перегонять данные из модели
    # MeSchema(**user)
    class Config:
        from_attributes = True


class PaginationSchema(SchemaBase):
    """📄 Схема пагинации для постраничного вывода"""
    page: Annotated[int, Field(ge=1, le=1000)] = 1
    limit: Annotated[int, Field(ge=1, le=100)] = 10

    @validator('page')
    def validate_page(cls, v):
        if v < 1:
            raise ValueError('Page must be greater than 0')
        return v

    @validator('limit')
    def validate_limit(cls, v):
        if v < 1:
            raise ValueError('Limit must be greater than 0')
        return v
