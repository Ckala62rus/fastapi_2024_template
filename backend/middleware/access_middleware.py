import traceback
from datetime import datetime

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi import Request, Response

from common.log import log
from utils.timezone import timezone


class AccessMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            start_time = timezone.now()
            response = await call_next(request)
            end_time = timezone.now()
            log.info(f'{response.status_code} {request.client.host} {request.method} {request.url} {end_time - start_time}')
            return response
        except Exception as e:
            log.error(f'{request.client.host} {request.method} {request.url}')
            log.error(traceback.format_exc())
            return Response(status_code=500)
