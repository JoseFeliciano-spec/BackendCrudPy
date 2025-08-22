from fastapi import APIRouter, HTTPException, status, Query
from typing import List

from app.features.products.domain.entities.product import ProductOut, ProductCreate, ProductUpdate
from app.features.products.dependency import ProductServiceDep, CurrentUserIdDep

router = APIRouter(prefix="/v1/products", tags=["products"])

@router.post("", response_model=ProductOut, status_code=201)
async def create_product(user_id: CurrentUserIdDep, payload: ProductCreate, svc: ProductServiceDep):
    return await svc.create(user_id, payload)

@router.get("", response_model=List[ProductOut])
async def list_products(
    user_id: CurrentUserIdDep,
    svc: ProductServiceDep,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100)
):
    print(user_id);
    return await svc.list(user_id, skip, limit)

@router.get("/{product_id}", response_model=ProductOut)
async def get_product(user_id: CurrentUserIdDep, product_id: str, svc: ProductServiceDep):
    prod = await svc.get(user_id, product_id)
    if not prod:
        raise HTTPException(status_code=404, detail="No encontrado")
    return prod

@router.put("/{product_id}", response_model=ProductOut)
async def update_product(user_id: CurrentUserIdDep, product_id: str, payload: ProductUpdate, svc: ProductServiceDep):
    updated = await svc.update(user_id, product_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="No encontrado")
    return updated

@router.delete("/{product_id}", status_code=204)
async def delete_product(user_id: CurrentUserIdDep, product_id: str, svc: ProductServiceDep):
    ok = await svc.delete(user_id, product_id)
    if not ok:
        raise HTTPException(status_code=404, detail="No encontrado")
    return
