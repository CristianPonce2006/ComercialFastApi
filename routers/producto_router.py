from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Query

from models.producto import Producto, ProductoCreate, ProductoUpdate
from models.categoria import Categoria
from sqlmodel import select
from config.session_dependencia import SessionDeDependencia

router = APIRouter()

@router.get("/productos", response_model=list[Producto], status_code=status.HTTP_200_OK)
async def get_productos(session: SessionDeDependencia, offset: int = Query(0, ge=0), limit: int = Query(20, ge=1)):
    consulta = select(Producto).offset(offset).limit(limit)
    resultado_consulta = session.exec(consulta)
    return resultado_consulta.all()

@router.get("/productos/{id}", response_model=Producto, status_code=status.HTTP_200_OK)
async def get_producto(id: int, session: SessionDeDependencia):
    consulta = select(Producto).where(Producto.id == id)
    resultado_consulta = session.exec(consulta).first()
    if not resultado_consulta:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return resultado_consulta

@router.post("/productos", response_model=Producto, status_code=status.HTTP_201_CREATED)
async def create_producto(datos: ProductoCreate, session: SessionDeDependencia):
    categoria = session.get(Categoria, datos.id_categoria)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")

    producto_nuevo = Producto(
        nombre=datos.nombre,
        descripcion=datos.descripcion,
        precio_compra=datos.precio_compra,
        precio_venta=datos.precio_venta,
        stock=datos.stock,
        image=datos.image,
        id_categoria=datos.id_categoria
    )
    session.add(producto_nuevo)
    session.commit()
    session.refresh(producto_nuevo)
    return producto_nuevo

@router.delete("/productos/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_producto(id: int, session: SessionDeDependencia):
    consulta = select(Producto).where(
        Producto.id == id
    )
    resultado_consulta = session.exec(consulta).first()
    if not resultado_consulta:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    session.delete(resultado_consulta)
    session.commit()
    return None

@router.put("/productos/{id}", response_model=Producto, status_code=status.HTTP_200_OK)
async def update_producto(id: int, datos_producto: ProductoUpdate, session: SessionDeDependencia):
    consulta = select(Producto).where(Producto.id == id)
    resultado_de_consulta = session.exec(consulta).first()

    if not resultado_de_consulta:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    categoria = session.get(Categoria, datos_producto.id_categoria)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")

    resultado_de_consulta.nombre = datos_producto.nombre
    resultado_de_consulta.descripcion = datos_producto.descripcion
    resultado_de_consulta.precio_compra = datos_producto.precio_compra
    resultado_de_consulta.precio_venta = datos_producto.precio_venta
    resultado_de_consulta.stock = datos_producto.stock
    resultado_de_consulta.image = datos_producto.image
    resultado_de_consulta.id_categoria = datos_producto.id_categoria

    resultado_de_consulta.update_at = datetime.now()
    session.add(resultado_de_consulta)
    session.commit()
    session.refresh(resultado_de_consulta)
    return resultado_de_consulta
