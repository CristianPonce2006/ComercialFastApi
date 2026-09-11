from sqlmodel import SQLModel, Field, Column, Numeric
from typing import Optional
from decimal import Decimal
from datetime import datetime
from pydantic import EmailStr
from decimal import Decimal

class DetalleVentaBase(SQLModel):
    id_venta: int = Field(nullable=False, foreign_key="ventas.id")
    id_producto: int = Field(nullable=False, foreign_key="productos.id")
    cantidad: int = Field(nullable=False, max_length=20, min_length=1)
    precio_unitario: Decimal = Field(sa_column=Column(Numeric(10, 2), nullable=False))
    subtotal: Decimal = Field(sa_column=Column(Numeric(10, 2), nullable=False))

class DetalleVenta(DetalleVentaBase, table=True):
    __tablename__ = "detalle_ventas" #type: ignore
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default_factory=datetime.now)
    updated_at: datetime | None = Field(default_factory=datetime.now)

class DetalleVentaCreate(DetalleVentaBase):
    pass

class DetalleVentaUpdate(DetalleVentaBase):
    pass