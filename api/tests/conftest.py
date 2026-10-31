import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.buro_falso import buro
from app.db import Base, get_db
from app.main import app
from app.models import Cliente

URL = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql+psycopg://credito:credito@localhost:5432/mini_credito_test",
)
engine = create_engine(URL)
SesionDePrueba = sessionmaker(bind=engine, expire_on_commit=False)


@pytest.fixture(scope="session", autouse=True)
def esquema():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield


@pytest.fixture(autouse=True)
def base_limpia():
    tablas = ", ".join(t.name for t in Base.metadata.sorted_tables)
    with engine.begin() as con:
        con.execute(text(f"TRUNCATE {tablas} RESTART IDENTITY CASCADE"))
    with SesionDePrueba() as db:
        db.add_all(
            [
                Cliente(nombre="Ana", email="ana@ejemplo.com", cedula="41234567"),
                Cliente(nombre="Bruno", email="bruno@ejemplo.com", cedula="38765432"),
            ]
        )
        db.commit()
    buro.demora_segundos = 0
    buro.consultas_cobradas = 0
    yield


@pytest.fixture
def db():
    with SesionDePrueba() as sesion:
        yield sesion


@pytest.fixture
def api():
    def get_db_de_prueba():
        with SesionDePrueba() as sesion:
            yield sesion

    app.dependency_overrides[get_db] = get_db_de_prueba
    with TestClient(app) as cliente:
        yield cliente
    app.dependency_overrides.clear()


ANA = {"X-Cliente-Id": "1"}
BRUNO = {"X-Cliente-Id": "2"}
