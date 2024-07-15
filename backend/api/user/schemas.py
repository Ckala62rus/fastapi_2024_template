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


class AuthSchemaCreate(AuthSchemaBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None


class AuthSchemaCreatedNewUser(SchemaBase):
    id: int
    email: EmailStr
    username: str
    created_at: datetime | None = None
    updated_at: datetime | None = None


class AuthLoginSchema(SchemaBase):
    email: EmailStr
    password: str | None
