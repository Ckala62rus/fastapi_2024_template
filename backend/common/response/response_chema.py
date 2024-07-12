#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Any

from fastapi import Response
from pydantic import BaseModel, ConfigDict

from common.response.response_code import CustomResponse, CustomResponseCode
from core.config import settings
from utils.serializer import MsgSpecJSONResponse

_ExcludeData = set[int | str] | dict[int | str, Any]

__all__ = ['ResponseModel', 'response_base']


class ResponseModel(BaseModel):
    """
    E.g. ::

        @router.get('/test', response_model=ResponseModel)
        def test():
            return ResponseModel(data={'test': 'test'})


        @router.get('/test')
        def test() -> ResponseModel:
            return ResponseModel(data={'test': 'test'})


        @router.get('/test')
        def test() -> ResponseModel:
            res = CustomResponseCode.HTTP_200
            return ResponseModel(code=res.code, msg=res.msg, data={'test': 'test'})
    """

    # TODO: json_encoders 配置失效: https://github.com/tiangolo/fastapi/discussions/10252
    model_config = ConfigDict(json_encoders={datetime: lambda x: x.strftime(settings.DATETIME_FORMAT)})

    code: int = CustomResponseCode.HTTP_200.code
    msg: str = CustomResponseCode.HTTP_200.msg
    data: Any | None = None


class ResponseBase:
    """
    E.g. ::
        @router.get('/test')
        def test() -> ResponseModel:
            return await response_base.success(data={'test': 'test'})
    """

    @staticmethod
    async def __response(*, res: CustomResponseCode | CustomResponse = None, data: Any | None = None) -> ResponseModel:
        """
        :param res:
        :param data:
        :return:
        """
        return ResponseModel(code=res.code, msg=res.msg, data=data)

    async def success(
        self,
        *,
        res: CustomResponseCode | CustomResponse = CustomResponseCode.HTTP_200,
        data: Any | None = None,
    ) -> ResponseModel:
        return await self.__response(res=res, data=data)

    async def fail(
        self,
        *,
        res: CustomResponseCode | CustomResponse = CustomResponseCode.HTTP_400,
        data: Any = None,
    ) -> ResponseModel:
        return await self.__response(res=res, data=data)

    @staticmethod
    async def fast_success(
        *,
        res: CustomResponseCode | CustomResponse = CustomResponseCode.HTTP_200,
        data: Any | None = None,
    ) -> Response:
        """
        .. warning::
        :param res:
        :param data:
        :return:
        """
        return MsgSpecJSONResponse({'code': res.code, 'msg': res.msg, 'data': data})


response_base = ResponseBase()
