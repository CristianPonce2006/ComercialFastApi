from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class CategoriaBase(SQLModel):
    nombre: str = Field(nullable=False, max_length=255, min_length=3)
    descripcion: Optional[str] = Field(default=None, max_length=255)


class Categoria(CategoriaBase, table=True):
    __tablename__ = "categorias" #type: ignore pa que no aparezca error
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default=datetime.now()) #lo cambie de utcnow a now porque daba error
    update_at: datetime | None = Field(default=datetime.now())

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaUpdate(CategoriaBase):
    pass