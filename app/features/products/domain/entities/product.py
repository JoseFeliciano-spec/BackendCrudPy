from pydantic import BaseModel, Field
from typing import Literal, Optional

Estado = Literal["activo", "inactivo", "borrador"]

class ProductBase(BaseModel):
    marca: str = Field(min_length=1, max_length=100)
    titulo: str = Field(min_length=1, max_length=200)
    estado: Estado

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    marca: Optional[str] = Field(default=None, min_length=1, max_length=100)
    titulo: Optional[str] = Field(default=None, min_length=1, max_length=200)
    estado: Optional[Estado] = None

class ProductOut(ProductBase):
    id: str
    owner_id: str
