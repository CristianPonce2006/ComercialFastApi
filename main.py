from fastapi import FastAPI, status
from contextlib import asynccontextmanager
from config.db import crear_db_y_tablas
from routers.categoria_router import router as categorias_router
from routers.producto_router import router as productos_router
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