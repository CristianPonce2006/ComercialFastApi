from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from pydantic import EmailStr

class UsuarioBase(SQLModel):
    username: str = Field(nullable=False, max_length=50, min_length=3, unique=True)
    password: str = Field(nullable=False, max_length=255, min_length=3)
    nombre: str = Field(nullable=False, max_length=100, min_length=3)
    apellido: str = Field(nullable=False, max_length=100, min_length=3)
    telefono: str = Field(nullable=False, max_length=9, min_length=9)
    correo: Optional[EmailStr] = Field(default=None, max_length=150)
    id_rol: int = Field(nullable=False, foreign_key="roles.id")
    

class Usuario(UsuarioBase, table=True):
    __tablename__ = "usuarios" #type: ignore pa que no aparezca error
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default_factory=datetime.now) #lo cambie de utcnow a now porque daba error
    updated_at: datetime | None = Field(default_factory=datetime.now)

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioUpdate(UsuarioBase):
    pass

class usuarioUpdatePatch(SQLModel):
    username: Optional[str] = Field(default=None, max_length=50, min_length=3)
    password: Optional[str] = Field(default=None, max_length=255, min_length=3)
    nombre: Optional[str] = Field(default=None, max_length=255, min_length=3)
    apellido: Optional[str] = Field(default=None, max_length=255, min_length=3)
    telefono: Optional[str] = Field(default=None, max_length=9, min_length=9)
    id_rol: Optional[int] = Field(default=None)
    correo: Optional[EmailStr] = Field(default=None, max_length=150)


