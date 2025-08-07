from contextlib import asynccontextmanager

from fastapi import FastAPI

__all__ = ['register_app']

from starlette.middleware.cors import CORSMiddleware

from core.config import settings
from core.path_conf import STATIC_DIR

from middleware.access_middleware import AccessMiddleware

from utils.serializer import MsgSpecJSONResponse
from api.router import router as main_router


@asynccontextmanager
async def register_init(app: FastAPI):
    """
    Жизненный цикл FastApi. Сдесь можно закрывать соединения с БД, Redis

    :return:
    """
    print("Run app")

    yield

    print("Stop app")
    #await redis_client.close()


def register_app():
    # FastAPI с улучшенной документацией
    app = FastAPI(
        title="🚀 FastAPI Architecture 2024",
        version="1.0.0",
        description="""
## 🎯 **FastAPI Best Architecture Project**

Современный, масштабируемый REST API, построенный с использованием лучших практик FastAPI.

### ✨ **Основные возможности:**

- 🔐 **JWT Авторизация** - Безопасная аутентификация и авторизация пользователей
- 👥 **Управление пользователями** - Полный CRUD для пользователей с ролями
- 🛡️ **Система разрешений** - Гибкая система управления правами доступа  
- 📊 **Пагинация** - Эффективная пагинация для больших наборов данных
- 🗃️ **PostgreSQL + Redis** - Надежное хранение данных и кэширование
- 📁 **MinIO Integration** - Управление файлами и объектным хранилищем
- 🍃 **MongoDB Support** - Поддержка NoSQL базы данных
- ⚡ **Celery Tasks** - Асинхронные фоновые задачи
- 🧪 **100% Test Coverage** - Полное покрытие тестами
- 📚 **Rich Documentation** - Подробная API документация

### 🏗️ **Архитектура:**

- **Clean Architecture** - Разделение на слои (API, Service, Repository)
- **Type Safety** - Полная типизация с Pydantic
- **Error Handling** - Централизованная обработка ошибок  
- **Logging** - Структурированное логирование
- **Validation** - Комплексная валидация входных данных
- **Security** - Современные практики безопасности

### 🛠️ **Технологический стек:**

- **FastAPI** - Современный веб-фреймворк для API
- **SQLAlchemy 2.0** - ORM для работы с базой данных
- **Alembic** - Миграции базы данных
- **PostgreSQL** - Основная реляционная БД
- **Redis** - Кэширование и сессии
- **MongoDB** - NoSQL документо-ориентированная БД
- **MinIO** - S3-совместимое объектное хранилище
- **Celery** - Очереди задач
- **Docker** - Контейнеризация

### 📞 **Поддержка API:**

Наш API поддерживает стандартные HTTP методы и коды ответов.
Все эндпоинты документированы с примерами запросов и ответов.
        """,
        docs_url=settings.DOCS_URL,
        redoc_url=settings.REDOCS_URL,
        openapi_url=settings.OPENAPI_URL,
        default_response_class=MsgSpecJSONResponse,
        lifespan=register_init,
        contact={
            "name": "FastAPI Architecture Team",
            "url": "https://github.com/your-org/fastapi-architecture-2024",
            "email": "support@fastapi-architecture.com",
        },
        license_info={
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT",
        },
        servers=[
            {
                "url": "http://localhost:5001",
                "description": "🔧 Development server"
            },
            {
                "url": "https://api-staging.example.com",
                "description": "🧪 Staging server"
            },
            {
                "url": "https://api.example.com", 
                "description": "🚀 Production server"
            }
        ],
        tags_metadata=[
            {
                "name": "👤 Authentication",
                "description": "**Аутентификация и авторизация пользователей.** Включает регистрацию, вход, выход, обновление токенов и управление сессиями.",
            },
            {
                "name": "👥 Users",
                "description": "**Управление пользователями.** CRUD операции для пользователей, профили, списки пользователей с пагинацией.",
            },
            {
                "name": "🛡️ Permissions",
                "description": "**Система разрешений.** Создание, редактирование и удаление разрешений для контроля доступа к ресурсам.",
            },
            {
                "name": "📁 Files",
                "description": "**Управление файлами.** Загрузка, скачивание и управление файлами через MinIO объектное хранилище.",
            },
            {
                "name": "🍃 MongoDB",
                "description": "**NoSQL операции.** Работа с MongoDB документами и коллекциями.",
            },
            {
                "name": "⚡ Tasks",
                "description": "**Фоновые задачи.** Управление Celery задачами и мониторинг их выполнения.",
            },
            {
                "name": "🧪 Examples",
                "description": "**Примеры использования.** Демонстрационные эндпоинты для изучения возможностей API.",
            },
        ],
        # Схема безопасности для JWT авторизации
        components={
            "securitySchemes": {
                "BearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                    "description": """
                    🔐 **JWT Bearer Token Authentication**
                    
                    Для доступа к защищенным эндпоинтам используйте Bearer токен:
                    
                    1. Получите токен через эндпоинт `/api/v1/user/login`
                    2. Добавьте токен в заголовок: `Authorization: Bearer <your-token>`
                    3. Токен действует 2 минуты, используйте refresh токен для обновления
                    
                    **Пример заголовка:**
                    ```
                    Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
                    ```
                    """
                }
            }
        },
    )

    register_static_file(app)
    register_middleware(app)
    register_router(app)

    return app


def register_static_file(app: FastAPI):
    """
    nginx

    :param app:
    :return:
    """
    if settings.STATIC_FILES:
        import os

        from fastapi.staticfiles import StaticFiles

        if not os.path.exists(STATIC_DIR):
            os.mkdir(STATIC_DIR)
        app.mount('/static', StaticFiles(directory=STATIC_DIR), name='static')


def register_middleware(app: FastAPI):
    # Access log handler
    if settings.MIDDLEWARE_ACCESS:
        app.add_middleware(AccessMiddleware)

    # CORS: Always at the end
    if settings.MIDDLEWARE_CORS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )


def register_router(app: FastAPI):
    # register api endpoints here.
    app.include_router(main_router)
