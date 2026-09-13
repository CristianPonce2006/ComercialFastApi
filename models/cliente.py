from sqlmodel import SQLModel, Field
from typing import Optional
from decimal import Decimal
from datetime import datetime
from pydantic import EmailStr

class ClienteBase(SQLModel):
    nombre: str = Field(nullable=False, max_length=100, min_length=3)
    apellido: str = Field(nullable=False, max_length=100, min_length=3)
    telefono: str = Field(nullable=False, max_length=9, min_length=9)
    correo: str = Field(nullable=False, max_length=150, min_length=3)
    direccion: Optional[str] = Field(default=None, max_length=255)


class Cliente(ClienteBase, table=True):
    __tablename__ = "clientes" #type: ignore
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default_factory=datetime.now)
    updated_at: datetime | None = Field(default_factory=datetime.now)

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(ClienteBase):
    pass