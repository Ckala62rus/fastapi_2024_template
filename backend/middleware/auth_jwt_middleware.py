from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException

from common.security.jwt import decode_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=False)  # Disable auto_error to control manually

    async def __call__(self, request: Request):
        authorization = request.headers.get("Authorization")
        
        if not authorization:
            raise HTTPException(status_code=401, detail="Authentication error. Not 'Authorization' header")
        
        # Parse Authorization header manually to ensure 401 status codes
        try:
            scheme, token = authorization.split(" ", 1)
        except ValueError:
            raise HTTPException(status_code=401, detail="Invalid authorization header format")
        
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")
        
        if not token.strip():
            raise HTTPException(status_code=401, detail="Missing token")
            
        if not await self.verify_jwt(token, request):
            raise HTTPException(status_code=401, detail="Invalid token or expired token")
            
        return token

    async def verify_jwt(self, jwtoken: str, request: Request) -> bool:
        isTokenValid: bool = False

        try:
            payload = await decode_jwt(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
            request.state.user_id = payload["user_id"]
        return isTokenValid
