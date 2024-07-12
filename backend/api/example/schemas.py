from pydantic import fields

from common.schema import SchemaBase

__all__ = [
    'HelloSchemaRetrieve',
    'HelloSchemaCreated',
    'HelloSchemaUpdate'
]


class HelloSchemaBase(SchemaBase):
    name: str
    age: int
    phone: str | None = None


class HelloSchemaRetrieve(SchemaBase):
    id: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                }
            ]
        }
    }


class HelloSchemaCreated(HelloSchemaBase):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "age": 25,
                    "phone": "88005553535",
                }
            ]
        }
    }


class HelloSchemaUpdate(HelloSchemaBase):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "age": 25,
                    "phone": "88005553535",
                }
            ]
        }
    }
