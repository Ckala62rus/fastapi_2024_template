# Example Minio client

```python
# Пример использования
if __name__ == "__main__":
    minio_client = MinIOClient()
    bucket_name = "test-bucket"
    object_name = "test-file.txt"
    file_path = "test-file.txt"
    
    # Создаем бакет
    minio_client.create_bucket(bucket_name)
    
    # Загружаем файл
    with open(file_path, "w") as f:
        f.write("Hello, MinIO!")
    
    minio_client.upload_file(bucket_name, object_name, file_path)
    
    # Загружаем данные из памяти
    minio_client.upload_data(bucket_name, "memory-data.txt", b"Data from memory")
    
    # Получаем список объектов
    objects = minio_client.list_objects(bucket_name)
    print("Objects in bucket:", objects)
    
    # Получаем информацию о файле
    file_info = minio_client.get_file_info(bucket_name, object_name)
    print("File info:", file_info)
    
    # Генерируем временную ссылку
    presigned_url = minio_client.generate_presigned_url(bucket_name, object_name)
    print("Presigned URL:", presigned_url)
    
    # Скачиваем файл
    minio_client.download_file(bucket_name, object_name, "downloaded-file.txt")
    
    # Скачиваем данные в память
    data = minio_client.download_data(bucket_name, object_name)
    print("Downloaded data:", data.decode())
    
    # Удаляем файл
    minio_client.delete_file(bucket_name, object_name)
    
    # Удаляем бакет (должен быть пустым)
    minio_client.delete_bucket(bucket_name)
```

### Ключевые особенности реализации:

1. Поддержка как файлов, так и данных в памяти:

   - upload_file/download_file - работа с файлами на диске
   - upload_data/download_data - работа с данными в памяти


2. Безопасность:


    - Использование .env для хранения учетных данных
    - Обработка ошибок для всех операций


3. Дополнительные функции:


    - Генерация временных ссылок (presigned_url)
    - Получение метаданных объектов
    - Рекурсивный список объектов


4. Best Practices:


    - Проверка существования бакетов перед операциями
    - Закрытие соединений после загрузки/скачивания
    - Логирование операций


5. Пример использования:


    - Демонстрация всех CRUD операций
    - Работа как с файлами, так и с данными в памяти

#### Для работы с этим кодом вам нужно иметь запущенный экземпляр MinIO с указанными в .env учетными данными.
