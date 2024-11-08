__all__ = [
    'FileUrl',
    'GetFile',
]

from common.schema import SchemaBase


class FileBase(SchemaBase):
    file: str
    bucket: str


class Bucket(SchemaBase):
    bucket: str | None = None


class FileUrl(FileBase):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "file": "car.jpg",
                    "bucket": "images",
                }
            ]
        }
    }


class GetFile(FileBase):
    bucket: str | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "file": "car.jpg",
                    "bucket": "images",
                }
            ]
        }
    }


class FilesSchema(SchemaBase):
    urls: list[str] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "code": 200,
                    "msg": "OK",
                    "data": {
                        "urls": [
                        "http://localhost:8001/api/v1/minio/file?file=71509ed8-01ce-445c-b16d-68ee41af436d-.jpg",
                        "http://localhost:8001/api/v1/minio/file?file=71509ed8-01ce-445c-b16d-68ee41af436d-.jpg",
                        "http://localhost:8001/api/v1/minio/file?file=71509ed8-01ce-445c-b16d-68ee41af436d-.jpg",
                        "http://localhost:8001/api/v1/minio/file?file=71509ed8-01ce-445c-b16d-68ee41af436d-.jpg",
                    ],
                    }
                }
            ]
        }
    }
