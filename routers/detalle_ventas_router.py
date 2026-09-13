from datetime import datetime

from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import select

from config.security_dependencia import Token_Dependencia
from config.session_dependencia import SessionDeDependencia
from models.detalle_venta import DetalleVenta, DetalleVentaCreate, DetalleVentaUpdate
from models.producto import Producto
from models.ventas import Venta

router = APIRouter(prefix="/detalle-ventas", tags=["detalle-ventas"])


def validar_venta(session: SessionDeDependencia, id_venta: int, token: dict) -> Venta:
    venta = session.get(Venta, id_venta)
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    if token.get("id_rol") == 2:
        if venta.id_usuario != token.get("id"):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="La venta no pertenece al vendedor")
    return venta


def validar_rol(token: dict) -> None:
    if token.get("id_rol") not in (1, 2):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Rol no autorizado")


def validar_producto(session: SessionDeDependencia, id_producto: int) -> None:
    if not session.get(Producto, id_producto):
        raise HTTPException(status_code=404, detail="Producto no encontrado")


@router.get("", response_model=list[DetalleVenta], status_code=status.HTTP_200_OK)
async def get_detalles(session: SessionDeDependencia, token: Token_Dependencia, offset: int = Query(0, ge=0), limit: int = Query(20, ge=1)):
    validar_rol(token)
    detalles = session.exec(select(DetalleVenta).offset(offset).limit(limit)).all()
    for detalle in detalles:
        validar_venta(session, detalle.id_venta, token)
    return detalles


@router.get("/{id}", response_model=DetalleVenta, status_code=status.HTTP_200_OK)
async def get_detalle(id: int, session: SessionDeDependencia, token: Token_Dependencia):
    validar_rol(token)
    detalle = session.get(DetalleVenta, id)
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle de venta no encontrado")
    validar_venta(session, detalle.id_venta, token)
    return detalle


@router.post("", response_model=DetalleVenta, status_code=status.HTTP_201_CREATED)
async def create_detalle(datos: DetalleVentaCreate, session: SessionDeDependencia, token: Token_Dependencia):
    validar_rol(token)
    validar_venta(session, datos.id_venta, token)
    validar_producto(session, datos.id_producto)
    detalle = DetalleVenta(**datos.model_dump())
    session.add(detalle)
    session.commit()
    session.refresh(detalle)
    return detalle


@router.put("/{id}", response_model=DetalleVenta, status_code=status.HTTP_200_OK)
async def update_detalle(id: int, datos: DetalleVentaUpdate, session: SessionDeDependencia, token: Token_Dependencia):
    validar_rol(token)
    detalle = session.get(DetalleVenta, id)
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle de venta no encontrado")
    validar_venta(session, detalle.id_venta, token)
    if datos.id_venta != detalle.id_venta:
        validar_venta(session, datos.id_venta, token)
    validar_producto(session, datos.id_producto)
    for campo, valor in datos.model_dump().items():
        setattr(detalle, campo, valor)
    detalle.updated_at = datetime.now()
    session.add(detalle)
    session.commit()
    session.refresh(detalle)
    return detalle


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_detalle(id: int, session: SessionDeDependencia, token: Token_Dependencia):
    validar_rol(token)
    detalle = session.get(DetalleVenta, id)
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle de venta no encontrado")
    validar_venta(session, detalle.id_venta, token)
    session.delete(detalle)
    session.commit()
    return None
