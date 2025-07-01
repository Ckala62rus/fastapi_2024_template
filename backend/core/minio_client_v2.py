import os
from datetime import timedelta
from dotenv import load_dotenv
from minio import Minio
from minio.error import S3Error
from io import BytesIO

from core.config import settings


class MinIOClient:
    def __init__(self):
        self.client = Minio(
            settings.MINIO_HOST,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.SECURE
        )

    def bucket_exists(self, bucket_name: str) -> bool:
        """Проверяет существование бакета"""
        try:
            return self.client.bucket_exists(bucket_name)
        except S3Error as e:
            print(f"Error checking bucket: {e}")
            return False

    def create_bucket(self, bucket_name: str) -> bool:
        """Создает новый бакет"""
        try:
            if not self.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name)
                print(f"Bucket {bucket_name} created successfully")
                return True
            print(f"Bucket {bucket_name} already exists")
            return False
        except S3Error as e:
            print(f"Error creating bucket: {e}")
            return False

    def upload_file(self, bucket_name: str, object_name: str, file_path: str,
                    content_type="application/octet-stream") -> bool:
        """
        Загружает файл в MinIO

        Args:
            bucket_name: Имя бакета
            object_name: Имя объекта в хранилище
            file_path: Путь к локальному файлу
            content_type: MIME-тип содержимого
        """
        try:
            self.client.fput_object(
                bucket_name,
                object_name,
                file_path,
                content_type=content_type
            )
            print(f"File {file_path} uploaded as {object_name}")
            return True
        except S3Error as e:
            print(f"Error uploading file: {e}")
            return False

    def upload_data(self, bucket_name: str, object_name: str, data: bytes,
                    content_type="application/octet-stream") -> bool:
        """
        Загружает данные из памяти в MinIO

        Args:
            bucket_name: Имя бакета
            object_name: Имя объекта в хранилище
            data: Данные для загрузки (bytes)
            content_type: MIME-тип содержимого
        """
        try:
            data_stream = BytesIO(data)
            self.client.put_object(
                bucket_name,
                object_name,
                data_stream,
                length=len(data),
                content_type=content_type
            )
            print(f"Data uploaded as {object_name}")
            return True
        except S3Error as e:
            print(f"Error uploading data: {e}")
            return False

    def download_file(self, bucket_name: str, object_name: str, file_path: str) -> bool:
        """
        Скачивает файл из MinIO

        Args:
            bucket_name: Имя бакета
            object_name: Имя объекта в хранилище
            file_path: Путь для сохранения файла
        """
        try:
            self.client.fget_object(bucket_name, object_name, file_path)
            print(f"File {object_name} downloaded to {file_path}")
            return True
        except S3Error as e:
            print(f"Error downloading file: {e}")
            return False

    def download_data(self, bucket_name: str, object_name: str) -> bytes:
        """
        Скачивает данные из MinIO в память

        Args:
            bucket_name: Имя бакета
            object_name: Имя объекта в хранилище

        Returns:
            bytes: Содержимое файла или None при ошибке
        """
        try:
            response = self.client.get_object(bucket_name, object_name)
            data = response.read()
            response.close()
            response.release_conn()
            return data
        except S3Error as e:
            print(f"Error downloading data: {e}")
            return None

    def list_objects(self, bucket_name: str, prefix: str = "") -> list:
        """
        Возвращает список объектов в бакете

        Args:
            bucket_name: Имя бакета
            prefix: Префикс для фильтрации объектов
        """
        try:
            objects = self.client.list_objects(bucket_name, prefix=prefix, recursive=True)
            return [obj.object_name for obj in objects]
        except S3Error as e:
            print(f"Error listing objects: {e}")
            return []

    def get_file_info(self, bucket_name: str, object_name: str) -> dict:
        """
        Возвращает метаданные объекта

        Args:
            bucket_name: Имя бакета
            object_name: Имя объекта в хранилище

        Returns:
            dict: Метаданные объекта или None при ошибке
        """
        try:
            stat = self.client.stat_object(bucket_name, object_name)
            return {
                "size": stat.size,
                "content_type": stat.content_type,
                "last_modified": stat.last_modified,
                "metadata": stat.metadata
            }
        except S3Error as e:
            print(f"Error getting file info: {e}")
            return None

    def generate_presigned_url(self, bucket_name: str, object_name: str, expires: int = 604800) -> str:
        """
        Генерирует временную ссылку для доступа к объекту

        Args:
            bucket_name: Имя бакета
            object_name: Имя объекта в хранилище
            expires: Время жизни ссылки в секундах (по умолчанию 7 дней)

        Returns:
            str: Временная ссылка или None при ошибке
        """
        try:
            return self.client.presigned_get_object(
                bucket_name,
                object_name,
                expires=timedelta(seconds=expires)
            )
        except S3Error as e:
            print(f"Error generating presigned URL: {e}")
            return None

    def delete_file(self, bucket_name: str, object_name: str) -> bool:
        """
        Удаляет объект из хранилища

        Args:
            bucket_name: Имя бакета
            object_name: Имя объекта в хранилище
        """
        try:
            self.client.remove_object(bucket_name, object_name)
            print(f"File {object_name} deleted successfully")
            return True
        except S3Error as e:
            print(f"Error deleting file: {e}")
            return False

    def delete_bucket(self, bucket_name: str) -> bool:
        """
        Удаляет бакет (должен быть пустым)

        Args:
            bucket_name: Имя бакета
        """
        try:
            self.client.remove_bucket(bucket_name)
            print(f"Bucket {bucket_name} deleted successfully")
            return True
        except S3Error as e:
            print(f"Error deleting bucket: {e}")
            return False