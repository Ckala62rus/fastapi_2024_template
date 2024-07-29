import sys

from redis import Redis
from redis.exceptions import (
    TimeoutError,
    AuthenticationError
)

from common.log import log
from core.config import settings


class RedisCli(Redis):
    def __init__(self):
        super(RedisCli, self).__init__(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            db=settings.REDIS_DATABASE,
            socket_timeout=settings.REDIS_TIMEOUT,
            decode_responses=True,  # Кодировка utf-8
        )

    async def open(self):
        """
        Инициализация

        :return:
        """
        try:
            await self.ping()
        except TimeoutError:
            log.error('❌ Ошибка. Подключение к базе данных Redis')
            sys.exit()
        except AuthenticationError:
            log.error('❌ Ошибка. Не удалось выполнить аутентификацию соединения Redis с базой данных.')
            sys.exit()
        except Exception as e:
            log.error('❌ Ошибка. Неверное соединение с базой данных Redis {}', e)
            sys.exit()

    async def delete_prefix(self, prefix: str, exclude: str | list = None):
        """
        Удалить все ключи, указанные в предыдущем разделе.

        :param prefix:
        :param exclude:
        :return:
        """
        keys = []
        for key in self.scan_iter(match=f'{prefix}*'):
            if isinstance(exclude, str):
                if key != exclude:
                    keys.append(key)
            elif isinstance(exclude, list):
                if key not in exclude:
                    keys.append(key)
            else:
                keys.append(key)
        for key in keys:
            self.delete(key)


# Создание redis экземпляра
redis_client = RedisCli()