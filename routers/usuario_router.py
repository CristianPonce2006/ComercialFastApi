from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Query

from models.usuario import Usuario, UsuarioCreate, UsuarioUpdate
from sqlmodel import select
from models.rol import Rol
from config.session_dependencia import SessionDeDependencia
from lib.pwd import get_password_hash
router = APIRouter()

@router.get("/usuarios", response_model=list[Usuario], status_code=status.HTTP_200_OK)
async def get_usuarios(session: SessionDeDependencia, offset: int = Query(0, ge=0), limit: int =Query(20, ge=1)):
    consulta = select(Usuario).offset(offset).limit(limit)
    resultado_consulta = session.exec(consulta)
    return resultado_consulta.all()

@router.get("/usuarios/{id}", response_model=Usuario, status_code=status.HTTP_200_OK)
async def get_Usuario(id: int,session: SessionDeDependencia):
    consulta = select(Usuario).where(Usuario.id == id)
    resultado_consulta = session.exec(consulta).first() #no olvidar el first
    if not resultado_consulta:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return resultado_consulta

@router.post("/usuarios", response_model=Usuario, status_code=status.HTTP_201_CREATED)
async def create_Usuario(datos: UsuarioCreate, session: SessionDeDependencia):
    Usuario_nuevo = Usuario(
        username=datos.username,
        password=get_password_hash(datos.password),
        nombre=datos.nombre,
        apellido=datos.apellido,
        telefono=datos.telefono,
        correo=datos.correo,
        id_rol=datos.id_rol
        )
    consulta = select(Usuario).where(
        Usuario.username == datos.username
    )
    usuario_existente = session.exec(consulta).first()
    if usuario_existente:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario ya esta en uso")
    if datos.id_rol: 
        consulta = select(Rol).where(Rol.id == datos.id_rol)
        rol = session.exec(consulta).first()
        if not rol:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rol no encontrado")
    session.add(Usuario_nuevo)
    session.commit()
    session.refresh(Usuario_nuevo)
    return Usuario_nuevo
