from datetime import datetime

from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import select

from config.security_dependencia import Token_Dependencia
from config.session_dependencia import SessionDeDependencia
from models.cliente import Cliente, ClienteCreate, ClienteUpdate
from models.ventas import Venta

router = APIRouter(prefix="/clientes", tags=["clientes"])


def validar_lectura_escritura(token: dict) -> None:
    if token.get("id_rol") not in (1, 2):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Rol no autorizado")


def validar_admin(token: dict) -> None:
    if token.get("id_rol") != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo el Admin puede eliminar clientes")


@router.get("", response_model=list[Cliente], status_code=status.HTTP_200_OK)
async def get_clientes(session: SessionDeDependencia, token: Token_Dependencia, offset: int = Query(0, ge=0), limit: int = Query(20, ge=1)):
    validar_lectura_escritura(token)
    return session.exec(select(Cliente).offset(offset).limit(limit)).all()


@router.get("/{id}", response_model=Cliente, status_code=status.HTTP_200_OK)
async def get_cliente(id: int, session: SessionDeDependencia, token: Token_Dependencia):
    validar_lectura_escritura(token)
    cliente = session.get(Cliente, id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente


@router.post("", response_model=Cliente, status_code=status.HTTP_201_CREATED)
async def create_cliente(datos: ClienteCreate, session: SessionDeDependencia, token: Token_Dependencia):
    validar_lectura_escritura(token)
    cliente = Cliente(**datos.model_dump())
    session.add(cliente)
    session.commit()
    session.refresh(cliente)
    return cliente


@router.put("/{id}", response_model=Cliente, status_code=status.HTTP_200_OK)
async def update_cliente(id: int, datos: ClienteUpdate, session: SessionDeDependencia, token: Token_Dependencia):
    validar_lectura_escritura(token)
    cliente = session.get(Cliente, id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    for campo, valor in datos.model_dump().items():
        setattr(cliente, campo, valor)
    cliente.updated_at = datetime.now()
    session.add(cliente)
    session.commit()
    session.refresh(cliente)
    return cliente


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cliente(id: int, session: SessionDeDependencia, token: Token_Dependencia):
    validar_admin(token)
    cliente = session.get(Cliente, id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    if session.exec(select(Venta).where(Venta.id_cliente == id)).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se puede eliminar el cliente porque tiene ventas asociadas")
    session.delete(cliente)
    session.commit()
    return None
