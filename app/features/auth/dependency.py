from fastapi import Depends, HTTPException, status, Header
import jwt
from typing import Annotated, Optional
from app.core.security import decode_token
from app.features.auth.infrastructure.repositories.user_repository_mongo import UserRepositoryMongo
from app.features.auth.domain.services.auth_service import AuthService

def get_auth_service() -> AuthService:
    return AuthService(UserRepositoryMongo())

async def get_current_user_id(authorization: Optional[str] = Header(default=None)) -> str:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token requerido")
    token = authorization.split(" ", 1)[1]
    try:
        payload = decode_token(token)
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    sub = payload.get("sub")
    if not sub:
        raise HTTPException(status_code=401, detail="Token inválido")
    return sub

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
CurrentUserIdDep = Annotated[str, Depends(get_current_user_id)]
