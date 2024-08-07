from typing import List

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


class PermissionCreateSchema(PermissionSchema):
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
