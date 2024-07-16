# FastAPI Template Architecture

### Запуск приложения
> python main.py

### Документация 
http://localhost:8001/api/v1/docs

### Разные команды

(параметры запуска для uvicorn)
> --reload --host 0.0.0.0 --port 8001

### Структура директорий

| Описание                        | php            | fastapi_template_architecture |
|---------------------------------|----------------|-------------------------------|
| обработчик                      | controller     | api                           |
| классы валидации входных данных | dto            | schema                        |
| сервисы с бизнес логикой        | service + impl | service                       |
| классы для мапинга              | dao / mapper   | crud                          |
| модели (БД)                     | model / entity | model                         |


### Poetry

- Создание requirements.txt экспорта зависимостей без хэшей

> poetry export --without-hashes -f requirements.txt --output requirements.txt

или

> poetry export --without-hashes --format=requirements.txt > requirements.txt

### Docker
```
> (Пересборка контейнера, принудительная) => docker-compose up --build --force-recreate --renew-anon-volumes
> (Сборка контейнеров) => docker-compose build
> (Зайти в конкретный контейнер) => docker exec -ti backend_fastapi_2024 bash
> (Запуск контейнеров в фоне) => docker-compose up -d
> (Вывести список контейнеров остановленных и работающих) => docker ps -a
```

### Alembic
```Bash
alembic init migrations
alembic revision --autogenerate -m "init"
alembic upgrade head
alembic history
alembic downgrade 8ac14e223d1e
alembic downgrade -1 (удаление всех миграций)
```

### Todo
1. Добавить Celery
2. Фоновые задачи Celery
3. Celery Flower
4. Redis
5. RabbitMQ
6. Миграции Alembic (+)
7. Попробовать пересоздать контейнер на базе Slim
8. CRUD для MongoDB
9. GreadFS для MongoDB
10. Добавить SQLAlchemy (+)
11. Реализовать регистрацию пользователей. (+)
12. Тестирование


#### PGAdmin
- host name default => db_fastapi_2024
- login => postgres
- password => 123123


#### Testing

1. Создать базу test_db
2. Запуск тестов
```Bash
pytest -vs --disable-warnings
```
