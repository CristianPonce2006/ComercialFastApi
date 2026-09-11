from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class RolBase(SQLModel):
    nombre: str = Field(nullable=False, max_length=50, min_length=3)
    descripcion: Optional[str] = Field(default=None, max_length=255)

class Rol(RolBase, table=True):
    __tablename__ = "roles" #type: ignore pa que no aparezca error
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default_factory=datetime.now) #lo cambie de utcnow a now porque daba error
    updated_at: datetime | None = Field(default_factory=datetime.now)

class RolCreate(RolBase):
    pass

class RolUpdate(RolBase):
    pass