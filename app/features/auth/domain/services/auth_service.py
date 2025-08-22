from typing import Optional, Tuple
from app.features.auth.domain.repositories.user_repository import IUserRepository
from app.features.auth.domain.entities.user import UserCreate, UserLogin, User
from app.core.security import hash_password, verify_password, create_access_token

class AuthService:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    async def register(self, payload: UserCreate) -> Tuple[str,User]:
        existing = await self.repo.get_by_email(payload.email)
        if existing:
            raise ValueError("Email ya registrado")
        hashed = hash_password(payload.password)
        created = await self.repo.create(payload.email, hashed, payload.name)
        return create_access_token({"sub": created.id, "email": created.email}), User(id=created.id, email=created.email, created_at=created.created_at, name=created.name)

    async def login(self, payload: UserLogin) -> Tuple[str, User]:
        user = await self.repo.get_by_email(payload.email)
        if not user or not verify_password(payload.password, user.hashed_password):
            raise ValueError("Credenciales inválidas")
        return create_access_token({"sub": user.id, "email": user.email}), User(id=user.id, email=user.email, created_at=user.created_at, name=user.name)

    async def get_user(self, user_id: str) -> Optional[User]:
        u = await self.repo.get_by_id(user_id)
        if not u:
            return None
        return User(id=u.id, email=u.email, created_at=u.created_at, name=u.name)
