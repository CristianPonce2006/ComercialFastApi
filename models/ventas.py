from sqlmodel import SQLModel, Field, Column, Numeric
from typing import Optional
from decimal import Decimal
from datetime import datetime
from pydantic import EmailStr


class VentaBase(SQLModel):
    id_cliente: int = Field(nullable=False, foreign_key="clientes.id")
    id_usuario: int = Field(nullable=False, foreign_key="usuarios.id")
    id_tipo_pago: int = Field(nullable=False, foreign_key="tipo_pago.id")
    fecha: datetime = Field(nullable=False)
    total: Decimal = Field(sa_column=Column(Numeric(10, 2), nullable=False))

class Venta(VentaBase, table=True):
    __tablename__ = "ventas" #type: ignore
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default_factory=datetime.now)
    updated_at: datetime | None = Field(default_factory=datetime.now)

class VentaCreate(VentaBase):
    pass

class VentaUpdate(VentaBase):
    pass