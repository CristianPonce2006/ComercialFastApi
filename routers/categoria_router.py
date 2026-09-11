from datetime import datetime

from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import select

from config.security_dependencia import Token_Dependencia
from config.session_dependencia import SessionDeDependencia
from models.categoria import Categoria, CategoriaCreate, CategoriaUpdate
from models.producto import Producto

router = APIRouter()


def validar_lectura(token: dict) -> None:
    if token.get("id_rol") not in (1, 2):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Rol no autorizado")


def validar_admin(token: dict) -> None:
    if token.get("id_rol") != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo el Admin puede realizar esta operación")


@router.get("/categorias", response_model=list[Categoria], status_code=status.HTTP_200_OK)
async def get_categorias(session: SessionDeDependencia, token: Token_Dependencia, offset: int = Query(0, ge=0), limit: int = Query(20, ge=1)):
    validar_lectura(token)
    return session.exec(select(Categoria).offset(offset).limit(limit)).all()


@router.get("/categorias/{id}", response_model=Categoria, status_code=status.HTTP_200_OK)
async def get_categoria(id: int, session: SessionDeDependencia, token: Token_Dependencia):
    validar_lectura(token)
    categoria = session.get(Categoria, id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    return categoria


@router.post("/categorias", response_model=Categoria, status_code=status.HTTP_201_CREATED)
async def create_categoria(datos: CategoriaCreate, session: SessionDeDependencia, token: Token_Dependencia):
    validar_admin(token)
    categoria = Categoria(**datos.model_dump())
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria


@router.put("/categorias/{id}", response_model=Categoria, status_code=status.HTTP_200_OK)
async def update_categoria(id: int, datos_categoria: CategoriaUpdate, session: SessionDeDependencia, token: Token_Dependencia):
    validar_admin(token)
    categoria = session.get(Categoria, id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    categoria.nombre = datos_categoria.nombre
    categoria.descripcion = datos_categoria.descripcion
    categoria.update_at = datetime.now()
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria


@router.delete("/categorias/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_categoria(id: int, session: SessionDeDependencia, token: Token_Dependencia):
    validar_admin(token)
    categoria = session.get(Categoria, id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    if session.exec(select(Producto).where(Producto.id_categoria == id)).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se puede eliminar la categoría porque tiene productos asociados")
    session.delete(categoria)
    session.commit()
    return None
