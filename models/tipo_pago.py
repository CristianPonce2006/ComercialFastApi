from sqlmodel import SQLModel, Field
from typing import Optional
from decimal import Decimal
from datetime import datetime


class TipoPagoBase(SQLModel):
    nombre: str = Field(nullable=False, max_length=50, min_length=3)
    descripcion: Optional[str] = Field(default=None, max_length=255)


class TipoPago(TipoPagoBase, table=True):
    __tablename__ = "tipo_pago" #type: ignore
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default_factory=datetime.now)
    updated_at: datetime | None = Field(default_factory=datetime.now)

class TipoPagoCreate(TipoPagoBase):
    pass

class TipoPagoUpdate(TipoPagoBase):
    pass