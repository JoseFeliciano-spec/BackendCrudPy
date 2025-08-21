from typing import List, Optional
from app.features.products.domain.repositories.product_repository import IProductRepository
from app.features.products.domain.entities.product import ProductOut, ProductCreate, ProductUpdate

class ProductService:
    def __init__(self, repo: IProductRepository):
        self.repo = repo

    async def create(self, owner_id: str, data: ProductCreate) -> ProductOut:
        return await self.repo.create(owner_id, data)

    async def get(self, owner_id: str, product_id: str) -> Optional[ProductOut]:
        return await self.repo.get(owner_id, product_id)

    async def list(self, owner_id: str, skip: int = 0, limit: int = 50) -> List[ProductOut]:
        return await self.repo.list(owner_id, skip, limit)

    async def update(self, owner_id: str, product_id: str, data: ProductUpdate) -> Optional[ProductOut]:
        return await self.repo.update(owner_id, product_id, data)

    async def delete(self, owner_id: str, product_id: str) -> bool:
        return await self.repo.delete(owner_id, product_id)
