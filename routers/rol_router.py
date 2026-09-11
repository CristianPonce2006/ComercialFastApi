from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Query

from models.rol import Rol, RolCreate, RolUpdate
from sqlmodel import select
from config.session_dependencia import SessionDeDependencia

router = APIRouter()

@router.get("/roles", response_model=list[Rol], status_code=status.HTTP_200_OK)
async def get_roles(session: SessionDeDependencia, offset: int = Query(0, ge=0), limit: int =Query(20, ge=1)):
    consulta = select(Rol).offset(offset).limit(limit)
    resultado_consulta = session.exec(consulta)
    return resultado_consulta.all()

@router.get("/roles/{id}", response_model=Rol, status_code=status.HTTP_200_OK)
async def get_rol(id: int,session: SessionDeDependencia):
    consulta = select(Rol).where(Rol.id == id)
    resultado_consulta = session.exec(consulta).first() #no olvidar el first
    if not resultado_consulta:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return resultado_consulta

@router.post("/roles", response_model=Rol, status_code=status.HTTP_201_CREATED)
async def create_Rol(datos: RolCreate, session: SessionDeDependencia):
    rol_nuevo = Rol(
        nombre=datos.nombre,
        descripcion=datos.descripcion
        )
    session.add(rol_nuevo)
    session.commit()
    session.refresh(rol_nuevo)
    return rol_nuevo