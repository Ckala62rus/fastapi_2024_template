from typing import List, Annotated

from pydantic import Field, validator

from common.schema import SchemaBase
from models.permission import Permission


class PermissionSchema(SchemaBase):
    id: int
    name: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "name": "some_permission"
                }
            ]
        }
    }


class PermissionAllSchema(SchemaBase):
    permissions: List[Permission]


class PermissionCreateSchema(SchemaBase):
    name: Annotated[str, Field(min_length=1, max_length=20, pattern=r'^[a-zA-Z0-9_-]+$')]

    @validator('name')
    def validate_name(cls, v):
        if not v or v.isspace():
            raise ValueError('Permission name cannot be empty or contain only spaces')
        return v.strip()

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "some_permission"
                }
            ]
        }
    }
