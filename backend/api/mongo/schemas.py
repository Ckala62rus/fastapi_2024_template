from common.schema import SchemaBase

__all__ = ["UpdateDateMongoDBSchema"]


class UpdateDateMongoDBSchema(SchemaBase):
    name: str


class MongoPaginateSchema(SchemaBase):
    page_size: int = 10
    page_num: int = 1

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "page_size": 1,
                    "page_num": 1,
                }
            ]
        }
    }
