import unittest
import logging
from unittest.mock import patch, MagicMock

from common.security.jwt import sign_jwt, decode_jwt
from common.log import logger
from core.db_redis import RedisCli


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] ***** #%(levelname)-8s %(filename)s:'
                      '%(lineno)d - %(name)s:%(funcName)s - %(message)s'
)


class TestJWT(unittest.IsolatedAsyncioTestCase):
    # def setUp(self):
    #     logger.debug(f'seUp. is running \n')
    #
    # def tearDown(self):
    #     logger.debug(f'\n tearDown. test were finished')

    async def test_jwt(self):
        # arrange
        user_id = 7

        # act
        token_info = await sign_jwt(user_id=user_id)

        # assert
        self.assertEqual(user_id, token_info["user_id"])

    async def test_decode_jwt(self):
        # arrange
        user_id = 711
        token_info = await sign_jwt(user_id=user_id)

        # act
        with patch('common.security.jwt.redis_client') as redis_client:
            redis_client.get.return_value = "veryVerySecretKey"
            result = await decode_jwt(token_info["access_token"])
            logger.info(result)

        # assert
        self.assertEqual(user_id, token_info["user_id"])
