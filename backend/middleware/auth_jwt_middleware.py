from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException

from common.exception import errors
from common.security.jwt import decode_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        if not request.headers.get("Authorization"):
            raise errors.TokenError(msg='Authentication error. Not \'Authentication\' header')

        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not await self.verify_jwt(credentials.credentials, request):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    async def verify_jwt(self, jwtoken: str, request: Request) -> bool:
        isTokenValid: bool = False

        try:
            payload = await decode_jwt(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
            request.user_id = payload["user_id"]
        return isTokenValid
