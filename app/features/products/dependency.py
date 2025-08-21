from fastapi import Depends, HTTPException, status, Header
from typing import Annotated, Optional

from app.features.products.domain.services.product_service import ProductService
from app.features.products.infrastructure.repositories.product_repository_mongo import ProductMongoRepository

from app.core.security import decode_token
import jwt


def get_product_service() -> ProductService:
    # Inyecta el adaptador concreto (Mongo) al servicio de dominio
    return ProductService(ProductMongoRepository())


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


ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]
CurrentUserIdDep = Annotated[str, Depends(get_current_user_id)]
