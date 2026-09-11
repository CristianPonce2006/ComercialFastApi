from datetime import datetime

from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import select

from config.security_dependencia import Token_Dependencia
from config.session_dependencia import SessionDeDependencia
from lib.pwd import get_password_hash
from models.rol import Rol
from models.usuario import Usuario, UsuarioCreate, UsuarioUpdate, usuarioUpdatePatch

router = APIRouter()


def validar_rol_autorizado(token: dict) -> None:
    if token.get("id_rol") not in (1, 2):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Rol no autorizado")


def validar_acceso_usuario(token: dict, id: int) -> None:
    validar_rol_autorizado(token)
    if token.get("id_rol") == 2 and token.get("id") != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="El Vendedor solo puede consultar o actualizar su propio usuario")


def validar_rol(session: SessionDeDependencia, id_rol: int) -> None:
    if not session.get(Rol, id_rol):
        raise HTTPException(status_code=404, detail="Rol no encontrado")


@router.get("/usuarios", response_model=list[Usuario], status_code=status.HTTP_200_OK)
async def get_usuarios(session: SessionDeDependencia, token: Token_Dependencia, offset: int = Query(0, ge=0), limit: int = Query(20, ge=1)):
    validar_rol_autorizado(token)
    consulta = select(Usuario)
    if token.get("id_rol") == 2:
        consulta = consulta.where(Usuario.id == token.get("id"))
    return session.exec(consulta.offset(offset).limit(limit)).all()


@router.get("/usuarios/{id}", response_model=Usuario, status_code=status.HTTP_200_OK)
async def get_usuario(id: int, session: SessionDeDependencia, token: Token_Dependencia):
    validar_acceso_usuario(token, id)
    usuario = session.get(Usuario, id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.post("/usuarios", response_model=Usuario, status_code=status.HTTP_201_CREATED)
async def create_usuario(datos: UsuarioCreate, session: SessionDeDependencia, token: Token_Dependencia):
    if token.get("id_rol") != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo el Admin puede crear usuarios")
    if session.exec(select(Usuario).where(Usuario.username == datos.username)).first():
        raise HTTPException(status_code=400, detail="El usuario ya esta en uso")
    validar_rol(session, datos.id_rol)
    usuario = Usuario(**datos.model_dump())
    usuario.password = get_password_hash(datos.password)
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario


@router.put("/usuarios/{id}", response_model=Usuario, status_code=status.HTTP_200_OK)
async def update_usuario(id: int, datos: UsuarioUpdate, session: SessionDeDependencia, token: Token_Dependencia):
    validar_acceso_usuario(token, id)
    usuario = session.get(Usuario, id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if token.get("id_rol") == 2 and datos.id_rol != usuario.id_rol:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="El Vendedor no puede modificar el campo id_rol")
    if session.exec(select(Usuario).where(Usuario.username == datos.username, Usuario.id != id)).first():
        raise HTTPException(status_code=400, detail="El usuario ya esta en uso")
    validar_rol(session, datos.id_rol)
    for campo, valor in datos.model_dump().items():
        setattr(usuario, campo, get_password_hash(valor) if campo == "password" else valor)
    usuario.updated_at = datetime.now()
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario


@router.patch("/usuarios/{id}", response_model=Usuario, status_code=status.HTTP_200_OK)
async def patch_usuario(id: int, datos: usuarioUpdatePatch, session: SessionDeDependencia, token: Token_Dependencia):
    validar_acceso_usuario(token, id)
    usuario = session.get(Usuario, id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    cambios = datos.model_dump(exclude_unset=True)
    if token.get("id_rol") == 2 and "id_rol" in cambios:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="El Vendedor no puede modificar el campo id_rol")
    if "username" in cambios and session.exec(select(Usuario).where(Usuario.username == cambios["username"], Usuario.id != id)).first():
        raise HTTPException(status_code=400, detail="El usuario ya esta en uso")
    if "id_rol" in cambios:
        validar_rol(session, cambios["id_rol"])
    for campo, valor in cambios.items():
        setattr(usuario, campo, get_password_hash(valor) if campo == "password" else valor)
    usuario.updated_at = datetime.now()
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario


@router.delete("/usuarios/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(id: int, session: SessionDeDependencia, token: Token_Dependencia):
    if token.get("id_rol") != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo el Admin puede eliminar usuarios")
    usuario = session.get(Usuario, id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    session.delete(usuario)
    session.commit()
    return None
