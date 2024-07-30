from datetime import datetime

from pydantic import EmailStr

from common.schema import SchemaBase


class AuthSchemaBase(SchemaBase):
    email: EmailStr
    password: str | None
    username: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "admin@mail.ru",
                    "password": "123123",
                    "username": "admin"
                }
            ]
        }
    }


class AccessTokenBase(SchemaBase):
    access_token: str
    access_token_type: str = 'Bearer'
    access_token_expire_time: datetime


class GetLoginToken(AccessTokenBase):
    pass
    # refresh_token: str
    # refresh_token_type: str = 'Bearer'
    # refresh_token_expire_time: datetime


class AuthSchemaCreate(AuthSchemaBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None


class AuthSchemaCreatedNewUser(SchemaBase):
    id: int
    email: EmailStr
    username: str
    created_time: datetime | None = None
    updated_time: datetime | None = None


class AuthLoginSchema(SchemaBase):
    email: EmailStr
    password: str | None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "admin@mail.ru",
                    "password": "123123",
                }
            ]
        }
    }


class MeSchema(AuthSchemaCreatedNewUser):
    is_superuser: bool
    is_staff: bool

    # Для того, что бы можно было перегонять данные из модели
    # MeSchema(**user)
    class Config:
        orm_mode = True
