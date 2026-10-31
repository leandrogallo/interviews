import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select

from app.db import Base, SessionLocal, engine
from app.models import Cliente
from app.routers import clientes, ofertas

logging.basicConfig(level=logging.INFO)

CLIENTES_DE_PRUEBA = [
    Cliente(nombre="Ana", email="ana@ejemplo.com", cedula="41234567"),
    Cliente(nombre="Bruno", email="bruno@ejemplo.com", cedula="38765432"),
    Cliente(nombre="Carla", email="carla@ejemplo.com", cedula="52223334"),
]


def preparar_base() -> None:
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        if db.scalar(select(Cliente).limit(1)) is None:
            db.add_all(CLIENTES_DE_PRUEBA)
            db.commit()


@asynccontextmanager
async def ciclo_de_vida(_app: FastAPI):
    preparar_base()
    yield


app = FastAPI(title="Mini-crédito", lifespan=ciclo_de_vida)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(clientes.router)
app.include_router(ofertas.router)
