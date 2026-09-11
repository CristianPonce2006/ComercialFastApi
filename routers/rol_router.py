from datetime import datetime

from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import select

from config.security_dependencia import Token_Dependencia
from config.session_dependencia import SessionDeDependencia
from models.rol import Rol, RolCreate, RolUpdate
from models.usuario import Usuario

router = APIRouter()


@router.get("/roles", response_model=list[Rol], status_code=status.HTTP_200_OK)
async def get_roles(session: SessionDeDependencia, token: Token_Dependencia, offset: int = Query(0, ge=0), limit: int = Query(20, ge=1)):
    if token.get("id_rol") != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo el Admin puede leer roles")
    return session.exec(select(Rol).offset(offset).limit(limit)).all()


@router.get("/roles/{id}", response_model=Rol, status_code=status.HTTP_200_OK)
async def get_rol(id: int, session: SessionDeDependencia, token: Token_Dependencia):
    if token.get("id_rol") != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo el Admin puede leer roles")
    rol = session.get(Rol, id)
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol


@router.post("/roles", response_model=Rol, status_code=status.HTTP_201_CREATED)
async def create_rol(datos: RolCreate, session: SessionDeDependencia, token: Token_Dependencia):
    if token.get("id_rol") != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo el Admin puede crear roles")
    rol = Rol(nombre=datos.nombre, descripcion=datos.descripcion)
    session.add(rol)
    session.commit()
    session.refresh(rol)
    return rol


@router.put("/roles/{id}", response_model=Rol, status_code=status.HTTP_200_OK)
async def update_rol(id: int, datos: RolUpdate, session: SessionDeDependencia, token: Token_Dependencia):
    if token.get("id_rol") != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo el Admin puede actualizar roles")
    rol = session.get(Rol, id)
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    rol.nombre = datos.nombre
    rol.descripcion = datos.descripcion
    rol.updated_at = datetime.now()
    session.add(rol)
    session.commit()
    session.refresh(rol)
    return rol


@router.delete("/roles/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rol(id: int, session: SessionDeDependencia, token: Token_Dependencia):
    if token.get("id_rol") != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo el Admin puede eliminar roles")
    rol = session.get(Rol, id)
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    if session.exec(select(Usuario).where(Usuario.id_rol == id)).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se puede eliminar el rol porque tiene usuarios asociados")
    session.delete(rol)
    session.commit()
    return None
