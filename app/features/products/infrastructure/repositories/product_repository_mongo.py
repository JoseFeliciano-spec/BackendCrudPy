from typing import Optional, List
from bson import ObjectId
from app.core.db.mongo import get_db 
from app.features.products.domain.repositories.product_repository import IProductRepository
from app.features.products.domain.entities.product import ProductOut, ProductCreate, ProductUpdate

def _to_product(doc) -> ProductOut:
    return ProductOut(
        id=str(doc["_id"]),
        owner_id=str(doc["owner_id"]),
        marca=doc["marca"],
        titulo=doc["titulo"],
        estado=doc["estado"],
    )

class ProductMongoRepository(IProductRepository):
    collection = "products"

    async def create(self, owner_id: str, data: ProductCreate) -> ProductOut:
        db = await get_db()
        payload = data.model_dump()
        payload["owner_id"] = owner_id  # guardar como string (simple y consistente con tu user.id)
        res = await db[self.collection].insert_one(payload)
        payload["_id"] = res.inserted_id
        return _to_product(payload)

    async def get(self, owner_id: str, product_id: str) -> Optional[ProductOut]:
        db = await get_db()
        try:
            oid = ObjectId(product_id)
        except Exception:
            return None
        doc = await db[self.collection].find_one({"_id": oid, "owner_id": owner_id})
        return _to_product(doc) if doc else None

    async def list(self, owner_id: str, skip: int = 0, limit: int = 50) -> List[ProductOut]:
        db = await get_db()
        cursor = db[self.collection].find({"owner_id": owner_id}).skip(skip).limit(limit)
        return [_to_product(doc) async for doc in cursor]

    async def update(self, owner_id: str, product_id: str, data: ProductUpdate) -> Optional[ProductOut]:
        db = await get_db()
        try:
            oid = ObjectId(product_id)
        except Exception:
            return None
        update_data = {k: v for k, v in data.model_dump().items() if v is not None}
        if not update_data:
            return await self.get(owner_id, product_id)
        await db[self.collection].update_one({"_id": oid, "owner_id": owner_id}, {"$set": update_data})
        return await self.get(owner_id, product_id)

    async def delete(self, owner_id: str, product_id: str) -> bool:
        db = await get_db()
        try:
            oid = ObjectId(product_id)
        except Exception:
            return False
        res = await db[self.collection].delete_one({"_id": oid, "owner_id": owner_id})
        return res.deleted_count == 1
