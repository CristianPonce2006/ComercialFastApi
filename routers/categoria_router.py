from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Query

from models.categoria import Categoria, CategoriaCreate, CategoriaUpdate
from sqlmodel import select
from config.session_dependencia import SessionDeDependencia

router = APIRouter()

@router.get("/categorias", response_model=list[Categoria], status_code=status.HTTP_200_OK)
async def get_categorias(session: SessionDeDependencia, offset: int = Query(0, ge=0), limit: int =Query(20, ge=1)):
    consulta = select(Categoria).offset(offset).limit(limit)
    resultado_consulta = session.exec(consulta)
    return resultado_consulta.all()

@router.get("/categorias/{id}", response_model=Categoria, status_code=status.HTTP_200_OK)
async def get_categoria(id: int,session: SessionDeDependencia):
    consulta = select(Categoria).where(Categoria.id == id)
    resultado_consulta = session.exec(consulta)
    if not resultado_consulta:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    return resultado_consulta

@router.post("/categorias", response_model=Categoria, status_code=status.HTTP_201_CREATED)
async def create_categoria(datos: CategoriaCreate, session: SessionDeDependencia):
    categoria_nueva = Categoria(
        nombre=datos.nombre,
        descripcion=datos.descripcion
        )
    session.add(categoria_nueva)
    session.commit()
    session.refresh(categoria_nueva)
    return categoria_nueva

@router.delete("/categorias/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_categoria(id: int, session: SessionDeDependencia):
    consulta = select(Categoria).where(
        Categoria.id == id
    )
    resultado_consulta = session.exec(consulta).first()
    if not resultado_consulta:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    session.delete(resultado_consulta)
    session.commit()
    return None

@router.put("/categorias/{id}", response_model=Categoria, status_code=status.HTTP_200_OK)
async def update_categoria(id: int, datos_categoria: CategoriaUpdate, session: SessionDeDependencia):
    consulta = select(Categoria).where(Categoria.id == id)
    resultado_de_consulta = session.exec(consulta).first()

    if not resultado_de_consulta:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    resultado_de_consulta.nombre = datos_categoria.nombre
    if datos_categoria.descripcion is not None:
        resultado_de_consulta.descripcion = datos_categoria.descripcion

    resultado_de_consulta.update_at = datetime.now() #lo cambie aca tambien
    session.add(resultado_de_consulta)
    session.commit()
    session.refresh(resultado_de_consulta)
    return resultado_de_consulta

#paginaron


