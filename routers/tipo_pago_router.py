from datetime import datetime

from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import select

from config.security_dependencia import Token_Dependencia
from config.session_dependencia import SessionDeDependencia
from models.tipo_pago import TipoPago, TipoPagoCreate, TipoPagoUpdate
from models.ventas import Venta

router = APIRouter(prefix="/tipo-pago", tags=["tipo-pago"])


def validar_lectura(token: dict) -> None:
    if token.get("id_rol") not in (1, 2):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Rol no autorizado")


def validar_admin(token: dict) -> None:
    if token.get("id_rol") != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo el Admin puede modificar tipos de pago")


@router.get("", response_model=list[TipoPago], status_code=status.HTTP_200_OK)
async def get_tipos_pago(session: SessionDeDependencia, token: Token_Dependencia, offset: int = Query(0, ge=0), limit: int = Query(20, ge=1)):
    validar_lectura(token)
    return session.exec(select(TipoPago).offset(offset).limit(limit)).all()


@router.get("/{id}", response_model=TipoPago, status_code=status.HTTP_200_OK)
async def get_tipo_pago(id: int, session: SessionDeDependencia, token: Token_Dependencia):
    validar_lectura(token)
    tipo_pago = session.get(TipoPago, id)
    if not tipo_pago:
        raise HTTPException(status_code=404, detail="Tipo de pago no encontrado")
    return tipo_pago


@router.post("", response_model=TipoPago, status_code=status.HTTP_201_CREATED)
async def create_tipo_pago(datos: TipoPagoCreate, session: SessionDeDependencia, token: Token_Dependencia):
    validar_admin(token)
    tipo_pago = TipoPago(**datos.model_dump())
    session.add(tipo_pago)
    session.commit()
    session.refresh(tipo_pago)
    return tipo_pago


@router.put("/{id}", response_model=TipoPago, status_code=status.HTTP_200_OK)
async def update_tipo_pago(id: int, datos: TipoPagoUpdate, session: SessionDeDependencia, token: Token_Dependencia):
    validar_admin(token)
    tipo_pago = session.get(TipoPago, id)
    if not tipo_pago:
        raise HTTPException(status_code=404, detail="Tipo de pago no encontrado")
    tipo_pago.nombre = datos.nombre
    tipo_pago.descripcion = datos.descripcion
    tipo_pago.updated_at = datetime.now()
    session.add(tipo_pago)
    session.commit()
    session.refresh(tipo_pago)
    return tipo_pago


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tipo_pago(id: int, session: SessionDeDependencia, token: Token_Dependencia):
    validar_admin(token)
    tipo_pago = session.get(TipoPago, id)
    if not tipo_pago:
        raise HTTPException(status_code=404, detail="Tipo de pago no encontrado")
    if session.exec(select(Venta).where(Venta.id_tipo_pago == id)).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se puede eliminar el tipo de pago porque está siendo utilizado en ventas")
    session.delete(tipo_pago)
    session.commit()
    return None
