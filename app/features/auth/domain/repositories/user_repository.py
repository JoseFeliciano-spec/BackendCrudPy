from abc import ABC, abstractmethod
from typing import Optional
from app.features.auth.domain.entities.user import UserInDB

class IUserRepository(ABC):
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[UserInDB]: ...
    @abstractmethod
    async def create(self, email: str, hashed_password: str, name: str) -> UserInDB: ...
    @abstractmethod
    async def get_by_id(self, user_id: str) -> Optional[UserInDB]: ...
