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
