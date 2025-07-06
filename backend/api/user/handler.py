from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException
)
from typing import Annotated
from fastapi.params import Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request
from loguru import logger

from api.user.schemas import (
    AuthSchemaBase,
    AuthSchemaCreate,
    AuthLoginSchema,
    PaginationSchema,
)
from api.user.service import (
    UserService,
    user_service
)
from common.response.response_chema import (
    response_base,
    ResponseModel
)
from common.response.response_code import CustomResponseCode
from core.db import get_db
# from middleware.PermissionChecker import PermissionChecker
from middleware.auth_jwt_middleware import JWTBearer

router = APIRouter()


@router.post(
    "/registration",
    summary="👤 Регистрация нового пользователя",
    description="""
    ## 🎯 **Регистрация пользователя в системе**
    
    Создает нового пользователя с указанными данными. 
    
    ### 📋 **Требования к данным:**
    - **Email**: Должен быть валидным и уникальным
    - **Password**: От 6 до 50 символов  
    - **Username**: От 2 до 20 символов (буквы, цифры, точки, тире, подчеркивания)
    
    ### ✅ **Успешный ответ:**
    Возвращает информацию о созданном пользователе с присвоенным ID и временными метками.
    
    ### ❌ **Возможные ошибки:**
    - **400**: Пользователь с таким email уже существует
    - **422**: Невалидные данные (неправильный формат email, слишком короткий пароль и т.д.)
    """,
    responses={
        status.HTTP_201_CREATED: {
            "description": "✅ Пользователь успешно зарегистрирован",
            "content": {
                "application/json": {
                    "example": {
                        "code": 201,
                        "msg": "Entity was created", 
                        "data": {
                            "id": 123,
                            "email": "newuser@example.com",
                            "username": "new_user",
                            "created_time": "2024-01-15T10:30:00+03:00",
                            "updated_time": None
                        }
                    }
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "❌ Пользователь с таким email уже существует",
            "content": {
                "application/json": {
                    "example": {
                        "code": 400,
                        "msg": "Bad Request",
                        "data": "User with newuser@example.com already exists"
                    }
                }
            }
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "🚫 Невалидные данные",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "type": "string_too_short",
                                "loc": ["body", "password"],
                                "msg": "String should have at least 6 characters",
                                "input": "123"
                            }
                        ]
                    }
                }
            }
        }
    },
    tags=["👤 Authentication"]
)
async def registration(
        credentials: Annotated[AuthSchemaBase, Body(
            description="Данные для регистрации пользователя",
            examples=[
                {
                    "email": "john.doe@company.com",
                    "password": "SecurePassword123",
                    "username": "john_doe"
                },
                {
                    "email": "alice.smith@example.com", 
                    "password": "MyPassword2024",
                    "username": "alice_smith"
                }
            ]
        )],
        db: AsyncSession = Depends(get_db)
) -> ResponseModel:
    try:
        created_user = await UserService().registration(credentials, db)
    except HTTPException as e:
        logger.info(f"Registration error: {e}")
        return await response_base.fail(
            res=CustomResponseCode.HTTP_400,
            data=f"User with {credentials.email} already exists"
        )
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return await response_base.fail(data=str(e))

    logger.info(f"User registered successfully: {created_user.dict}")
    return await response_base.success(
        res=CustomResponseCode.HTTP_201,
        data=created_user
    )


@router.post(
    "/login",
    summary="🔐 Вход в систему",
    description="""
    ## 🎯 **Аутентификация пользователя**
    
    Выполняет вход пользователя в систему по email и паролю.
    
    ### 🔑 **Возвращаемые токены:**
    - **Access Token**: Для доступа к защищенным ресурсам (срок действия: 2 минуты)
    - **Refresh Token**: Для обновления access токена (срок действия: 7 дней)
    
    ### 📋 **Процесс входа:**
    1. Проверка существования пользователя по email
    2. Верификация пароля
    3. Генерация JWT токенов
    4. Сохранение токенов в Redis
    
    ### 🔒 **Безопасность:**
    - Пароли хэшируются с использованием bcrypt
    - Токены подписываются секретным ключом
    - Поддержка отзыва токенов
    """,
    responses={
        status.HTTP_200_OK: {
            "description": "✅ Успешный вход в систему",
            "content": {
                "application/json": {
                    "example": {
                        "code": 200,
                        "msg": "Request was successful",
                        "data": {
                            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                            "access_token_type": "Bearer",
                            "access_token_expire_time": "2024-01-15T10:32:00+03:00",
                            "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                            "refresh_token_type": "Bearer", 
                            "refresh_token_expire_time": "2024-01-22T10:30:00+03:00"
                        }
                    }
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "❌ Неверные учетные данные",
            "content": {
                "application/json": {
                    "example": {
                        "code": 400,
                        "msg": "Bad Request", 
                        "data": "Invalid credentials"
                    }
                }
            }
        }
    },
    tags=["👤 Authentication"]
)
async def login(
        credentials: Annotated[AuthLoginSchema, Body(
            description="Учетные данные для входа",
            examples=[
                {
                    "email": "john.doe@company.com",
                    "password": "SecurePassword123"
                },
                {
                    "email": "admin@example.com",
                    "password": "AdminPassword2024"
                }
            ]
        )],
        db: AsyncSession = Depends(get_db)
) -> ResponseModel:
    try:
        result = await UserService().login(credentials, db)

        logger.info(f"Login successful for user: {credentials.email}")
        return await response_base.success(
            res=CustomResponseCode.HTTP_200,
            data=result.model_dump()
        )
    except HTTPException as e:
        logger.error(f"Login error: {e}")
        return await response_base.fail(
            res=CustomResponseCode.HTTP_400,
            data=f"Invalid credentials"
        )


@router.get(
    "/me",
    summary="👤 Получить профиль текущего пользователя",
    description="""
    ## 🎯 **Информация о текущем пользователе**
    
    Возвращает детальную информацию о профиле авторизованного пользователя.
    
    ### 🔐 **Требования:**
    - Валидный JWT токен в заголовке Authorization
    
    ### 📊 **Возвращаемые данные:**
    - Основная информация (ID, email, username)
    - Временные метки (дата создания и обновления)
    - Роли пользователя (is_superuser, is_staff)
    
    ### 🛡️ **Безопасность:**
    - Эндпоинт защищен JWT авторизацией
    - Пользователь может получить только свой профиль
    """,
    responses={
        status.HTTP_200_OK: {
            "description": "✅ Профиль пользователя получен успешно",
            "content": {
                "application/json": {
                    "example": {
                        "code": 200,
                        "msg": "Request was successful",
                        "data": {
                            "id": 123,
                            "email": "john.doe@company.com",
                            "username": "john_doe",
                            "created_time": "2024-01-15T10:30:00+03:00",
                            "updated_time": "2024-01-15T15:45:00+03:00",
                            "is_superuser": False,
                            "is_staff": False
                        }
                    }
                }
            }
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "🚫 Не авторизован - отсутствует или невалидный токен",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid token or expired token."
                    }
                }
            }
        }
    },
    dependencies=[Depends(JWTBearer())],
    tags=["👥 Users"]
)
async def me(
        request: Request,
        db: AsyncSession = Depends(get_db)
) -> ResponseModel:
    try:
        user = await UserService.me(request.state.user_id, db)
        return await response_base.success(
            res=CustomResponseCode.HTTP_200,
            data=user
        )
    except HTTPException as e:
        return await response_base.fail(
            res=CustomResponseCode.HTTP_400,
            data=f"Error /me route. {e}"
        )


@router.post(
    "/logout",
    summary="🚪 Выход из системы",
    description="""
    ## 🎯 **Завершение пользовательской сессии**
    
    Выполняет безопасный выход пользователя из системы.
    
    ### 🔄 **Процесс выхода:**
    1. Проверка валидности токена
    2. Удаление токенов из Redis кэша
    3. Логирование события выхода
    
    ### 🛡️ **Безопасность:**
    - Немедленная инвалидация всех токенов пользователя
    - Предотвращение повторного использования токенов
    - Защита от несанкционированного доступа
    
    ### ⚠️ **Важно:**
    После выхода все существующие токены становятся недействительными.
    """,
    responses={
        status.HTTP_200_OK: {
            "description": "✅ Успешный выход из системы",
            "content": {
                "application/json": {
                    "example": {
                        "code": 200,
                        "msg": "Request was successful",
                        "data": "Successfully logged out"
                    }
                }
            }
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "🚫 Не авторизован - отсутствует или невалидный токен",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid token or expired token."
                    }
                }
            }
        }
    },
    dependencies=[Depends(JWTBearer())],
    tags=["👤 Authentication"]
)
async def logout(
        request: Request
) -> ResponseModel:
    try:
        result = await user_service.logout(request=request)
        return await response_base.success(data=result)
    except Exception as e:
        logger.error(f"Logout error: {e}")
        return await response_base.fail(data=str(e))


@router.get(
    "/users",
    summary="📋 Получить список пользователей",
    description="""
    ## 🎯 **Получение списка всех пользователей**
    
    Возвращает постраничный список всех зарегистрированных пользователей.
    
    ### 📄 **Пагинация:**
    - **page**: Номер страницы (от 1 до 1000, по умолчанию: 1)
    - **limit**: Количество пользователей на страницу (от 1 до 100, по умолчанию: 10)
    
    ### 📊 **Возвращаемые данные:**
    - Массив пользователей с основной информацией
    - Поддержка больших объемов данных через пагинацию
    - Оптимизированные запросы к базе данных
    
    ### 🔍 **Применение:**
    - Административные панели
    - Списки участников
    - Аналитика и отчеты
    """,
    responses={
        status.HTTP_200_OK: {
            "description": "✅ Список пользователей получен успешно",
            "content": {
                "application/json": {
                    "example": {
                        "code": 200,
                        "msg": "Request was successful",
                        "data": [
                            {
                                "id": 1,
                                "email": "john.doe@company.com",
                                "username": "john_doe",
                                "created_time": "2024-01-15T10:30:00+03:00",
                                "updated_time": None,
                                "is_superuser": False,
                                "is_staff": False
                            },
                            {
                                "id": 2,
                                "email": "alice.smith@example.com", 
                                "username": "alice_smith",
                                "created_time": "2024-01-16T14:22:00+03:00",
                                "updated_time": "2024-01-16T16:45:00+03:00",
                                "is_superuser": False,
                                "is_staff": True
                            }
                        ]
                    }
                }
            }
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "🚫 Невалидные параметры пагинации",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "type": "greater_than_equal",
                                "loc": ["query", "page"],
                                "msg": "Input should be greater than or equal to 1",
                                "input": 0
                            }
                        ]
                    }
                }
            }
        }
    },
    tags=["👥 Users"]
)
async def get_users(
        pagination: Annotated[PaginationSchema, Depends()],
        db: AsyncSession = Depends(get_db)
) -> ResponseModel:
    try:
        users = await UserService().get_all_users(
            db,
            pagination.limit,
            pagination.page,
        )
        logger.info(f"Retrieved {len(users) if users else 0} users, page: {pagination.page}, limit: {pagination.limit}")
        return await response_base.success(
            res=CustomResponseCode.HTTP_200,
            data=users
        )
    except Exception as e:
        logger.error(f"Error retrieving users: {e}")
        return await response_base.fail(
            res=CustomResponseCode.HTTP_500,
            data=f"Failed to retrieve users: {e}"
        )


@router.post(
    "/token/refresh",
    summary="🔄 Обновление токенов",
    description="""
    ## 🎯 **Обновление JWT токенов**
    
    Генерирует новую пару токенов (access + refresh) используя действующий refresh токен.
    
    ### 🔄 **Процесс обновления:**
    1. Валидация переданного refresh токена
    2. Проверка существования токена в Redis
    3. Генерация новых access и refresh токенов
    4. Удаление старого refresh токена
    5. Сохранение новых токенов в Redis
    
    ### ⏰ **Время жизни токенов:**
    - **Access Token**: 2 минуты
    - **Refresh Token**: 7 дней
    
    ### 🛡️ **Безопасность:**
    - Одноразовое использование refresh токенов
    - Автоматическая ротация токенов
    - Защита от повторного использования
    """,
    responses={
        status.HTTP_200_OK: {
            "description": "✅ Токены успешно обновлены",
            "content": {
                "application/json": {
                    "example": {
                        "code": 200,
                        "msg": "Request was successful",
                        "data": {
                            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                            "access_token_type": "Bearer",
                            "access_token_expire_time": "2024-01-15T10:32:00+03:00",
                            "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                            "refresh_token_type": "Bearer",
                            "refresh_token_expire_time": "2024-01-22T10:30:00+03:00"
                        }
                    }
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "❌ Невалидный или истекший refresh токен",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid or expired refresh token"
                    }
                }
            }
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "🚫 Не авторизован - отсутствует access токен",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid authentication scheme"
                    }
                }
            }
        }
    },
    dependencies=[Depends(JWTBearer())],
    tags=["👤 Authentication"]
)
async def token_refresh(
        request: Request,
        refresh_token: Annotated[str, Query(
            description="Refresh токен для обновления",
            example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        )],
        db: AsyncSession = Depends(get_db)
) -> ResponseModel:
    try:
        result = await user_service.token_refresh(request=request, refresh_token=refresh_token, db=db)
        logger.info(f"Token refreshed successfully for user: {request.state.user_id}")
        return await response_base.success(
            res=CustomResponseCode.HTTP_200,
            data=result.model_dump()
        )
    except HTTPException as e:
        logger.error(f"Token refresh error: {e}")
        # Re-raise HTTPException to let FastAPI handle it with proper HTTP status
        if "Invalid refresh token" in str(e.detail):
            raise e  # Let FastAPI return HTTP 400
        return await response_base.fail(
            res=CustomResponseCode.HTTP_400,
            data=f"Token refresh failed: {e}"
        )
