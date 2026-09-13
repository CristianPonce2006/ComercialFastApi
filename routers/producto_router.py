from datetime import datetime

from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import select

from config.security_dependencia import Token_Dependencia
from config.session_dependencia import SessionDeDependencia
from models.categoria import Categoria
from models.producto import Producto, ProductoCreate, ProductoUpdate

router = APIRouter()


def validar_lectura(token: dict) -> None:
    if token.get("id_rol") not in (1, 2):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Rol no autorizado")


def validar_admin(token: dict) -> None:
    if token.get("id_rol") != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo el Admin puede realizar esta operación")


@router.get("/productos", response_model=list[Producto], status_code=status.HTTP_200_OK)
async def get_productos(session: SessionDeDependencia, token: Token_Dependencia, offset: int = Query(0, ge=0), limit: int = Query(20, ge=1)):
    validar_lectura(token)
    return session.exec(select(Producto).offset(offset).limit(limit)).all()


@router.get("/productos/{id}", response_model=Producto, status_code=status.HTTP_200_OK)
async def get_producto(id: int, session: SessionDeDependencia, token: Token_Dependencia):
    validar_lectura(token)
    producto = session.get(Producto, id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.post("/productos", response_model=Producto, status_code=status.HTTP_201_CREATED)
async def create_producto(datos: ProductoCreate, session: SessionDeDependencia, token: Token_Dependencia):
    validar_admin(token)
    if not session.get(Categoria, datos.id_categoria):
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    producto = Producto(**datos.model_dump())
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto


@router.put("/productos/{id}", response_model=Producto, status_code=status.HTTP_200_OK)
async def update_producto(id: int, datos: ProductoUpdate, session: SessionDeDependencia, token: Token_Dependencia):
    validar_admin(token)
    producto = session.get(Producto, id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    if not session.get(Categoria, datos.id_categoria):
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    for campo, valor in datos.model_dump().items():
        setattr(producto, campo, valor)
    producto.update_at = datetime.now()
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto


@router.delete("/productos/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_producto(id: int, session: SessionDeDependencia, token: Token_Dependencia):
    validar_admin(token)
    producto = session.get(Producto, id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    session.delete(producto)
    session.commit()
    return None
