from datetime import date, datetime

from pydantic import BaseModel


class ClienteOut(BaseModel):
    id: int
    nombre: str


class ElegibilidadOut(BaseModel):
    elegible: bool
    score: int


class OfertaIn(BaseModel):
    monto: float
    plazo_meses: int


class OfertaOut(BaseModel):
    id: int
    monto: float
    plazo_meses: int
    tea: float
    comision: float
    estado: str
    creada_en: datetime


class CuotaOut(BaseModel):
    numero: int
    vencimiento: date
    capital: float
    interes: float
    total: float
    dias_de_atraso: int
