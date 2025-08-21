from fastapi import APIRouter, HTTPException, status
from app.features.auth.domain.entities.user import UserCreate, UserLogin, User
from app.features.auth.dependency import AuthServiceDep, CurrentUserIdDep

router = APIRouter(prefix="/v1/auth", tags=["auth"])

@router.post("/register", response_model=User, status_code=201)
async def register(payload: UserCreate, svc: AuthServiceDep):
    try:
        return await svc.register(payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/login")
async def login(payload: UserLogin, svc: AuthServiceDep):
    try:
        token = await svc.login(payload)
        return {"access_token": token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@router.get("/me", response_model=User)
async def get_me(user_id: CurrentUserIdDep, svc: AuthServiceDep):
    user = await svc.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user
