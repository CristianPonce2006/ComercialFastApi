from fastapi import FastAPI, status
from contextlib import asynccontextmanager
from config.db import crear_db_y_tablas
from routers.categoria_router import router as categorias_router
from routers.producto_router import router as productos_router
from routers.rol_router import router as roles_router
from routers.usuario_router import router as usuarios_router
from oauth.oauth import router as oauth_router
from routers.clientes_router import router as clientes_router
from routers.ventas_router import router as ventas_router
from routers.tipo_pago_router import router as tipo_pago_router
from routers.detalle_ventas_router import router as detalle_ventas_router

import models

@asynccontextmanager
async def lifespan(app: FastAPI):
    crear_db_y_tablas()
    yield

app = FastAPI(lifespan=lifespan)
app.title = "API Tienda X"
app.version = "0.0.1"

@app.get("/", summary="Comprobando Api", status_code=status.HTTP_200_OK)
async def home():
    return {"message": "ok"}

app.include_router(categorias_router, tags=["categorias"])
app.include_router(productos_router, tags=["productos"])
app.include_router(roles_router, tags=["roles"])
app.include_router(usuarios_router, tags=['usuarios'])
app.include_router(oauth_router, tags=['oauth'])
app.include_router(clientes_router)
app.include_router(ventas_router)
app.include_router(tipo_pago_router)
app.include_router(detalle_ventas_router)