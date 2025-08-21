from typing import Optional
from bson import ObjectId
from datetime import datetime, timezone
from app.features.auth.domain.repositories.user_repository import IUserRepository
from app.features.auth.domain.entities.user import UserInDB
from app.core.db.mongo import get_db

def _to_user_in_db(doc) -> UserInDB:
    return UserInDB(
        id=str(doc["_id"]),
        email=doc["email"],
        hashed_password=doc["hashed_password"],
        created_at=doc["created_at"],
        name=doc["name"],
    )

class UserRepositoryMongo(IUserRepository):
    collection_name = "users"

    async def get_by_email(self, email: str) -> Optional[UserInDB]:
        db = await get_db()
        doc = await db[self.collection_name].find_one({"email": email})
        return _to_user_in_db(doc) if doc else None

    async def create(self, email: str, hashed_password: str, name: str) -> UserInDB:
        db = await get_db()
        payload = {
            "email": email,
            "hashed_password": hashed_password,
            "name": name,
            "created_at": datetime.now(timezone.utc),
        }
        res = await db[self.collection_name].insert_one(payload)
        payload["_id"] = res.inserted_id
        return _to_user_in_db(payload)

    async def get_by_id(self, user_id: str) -> Optional[UserInDB]:
        db = await get_db()
        try:
            oid = ObjectId(user_id)
        except Exception:
            return None
        doc = await db[self.collection_name].find_one({"_id": oid})
        return _to_user_in_db(doc) if doc else None
