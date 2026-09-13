from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import select

from config.security_dependencia import Token_Dependencia
from config.session_dependencia import SessionDeDependencia
from models.cliente import Cliente
from models.tipo_pago import TipoPago
from models.ventas import Venta, VentaCreate, VentaUpdate

router = APIRouter(prefix="/ventas", tags=["ventas"])


def validar_lectura(token: dict) -> None:
    if token.get("id_rol") not in (1, 2):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Rol no autorizado")


def obtener_id_usuario(token: dict) -> int:
    id_usuario = token.get("id")
    if not isinstance(id_usuario, int):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token sin un usuario válido")
    return id_usuario


def validar_fk(session: SessionDeDependencia, datos: VentaCreate | VentaUpdate) -> None:
    if not session.get(Cliente, datos.id_cliente):
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    if not session.get(TipoPago, datos.id_tipo_pago):
        raise HTTPException(status_code=404, detail="Tipo de pago no encontrado")


@router.get("", response_model=list[Venta], status_code=status.HTTP_200_OK)
async def get_ventas(session: SessionDeDependencia, token: Token_Dependencia, offset: int = Query(0, ge=0), limit: int = Query(20, ge=1)):
    validar_lectura(token)
    consulta = select(Venta)
    if token.get("id_rol") == 2:
        consulta = consulta.where(Venta.id_usuario == token.get("id"))
    return session.exec(consulta.offset(offset).limit(limit)).all()


@router.get("/{id}", response_model=Venta, status_code=status.HTTP_200_OK)
async def get_venta(id: int, session: SessionDeDependencia, token: Token_Dependencia):
    validar_lectura(token)
    venta = session.get(Venta, id)
    if not venta or (token.get("id_rol") == 2 and venta.id_usuario != token.get("id")):
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return venta


@router.post("", response_model=Venta, status_code=status.HTTP_201_CREATED)
async def create_venta(datos: VentaCreate, session: SessionDeDependencia, token: Token_Dependencia):
    validar_lectura(token)
    validar_fk(session, datos)
    venta = Venta(**datos.model_dump())
    venta.id_usuario = obtener_id_usuario(token)
    session.add(venta)
    session.commit()
    session.refresh(venta)
    return venta


@router.put("/{id}", response_model=Venta, status_code=status.HTTP_200_OK)
async def update_venta(id: int, datos: VentaUpdate, session: SessionDeDependencia, token: Token_Dependencia):
    validar_lectura(token)
    venta = session.get(Venta, id)
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    if token.get("id_rol") == 2:
        if venta.id_usuario != token.get("id"):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo puedes actualizar tus propias ventas")
    validar_fk(session, datos)
    venta.id_cliente = datos.id_cliente
    venta.id_tipo_pago = datos.id_tipo_pago
    venta.fecha = datos.fecha
    venta.total = datos.total
    session.add(venta)
    session.commit()
    session.refresh(venta)
    return venta


@router.delete("/{id}", status_code=status.HTTP_400_BAD_REQUEST)
async def delete_venta(id: int, session: SessionDeDependencia, token: Token_Dependencia):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Las ventas no deben eliminarse físicamente; deben anularse según las reglas de negocio",
    )
