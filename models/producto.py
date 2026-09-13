from sqlmodel import SQLModel, Field
from typing import Optional
from decimal import Decimal
from datetime import datetime

class ProductoBase(SQLModel):
    nombre: str = Field(nullable=False, max_length=100, min_length=4)
    descripcion: Optional[str] = Field(default=None, max_length=255)
    precio_compra: Decimal = Field(nullable=False, gt=0, max_digits=10, decimal_places=2)
    precio_venta: Decimal = Field(nullable=False, gt=0, max_digits=10, decimal_places=2)
    stock: int = Field(nullable=False, ge=0)
    image: str = Field(nullable=False, max_length=255)
    id_categoria: int = Field(nullable=False, foreign_key="categorias.id")
    
class Producto(ProductoBase, table=True):
    __tablename__ = "productos" #type: ignore pa que no aparezca error
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default_factory=datetime.now)
    update_at: datetime | None = Field(default_factory=datetime.now)

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(ProductoBase):
    pass