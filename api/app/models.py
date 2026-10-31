from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import JSON, DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


def ahora_utc() -> datetime:
    return datetime.now(timezone.utc)


class Cliente(Base):
    __tablename__ = "cliente"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(200), unique=True)
    cedula: Mapped[str] = mapped_column(String(8), unique=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=ahora_utc)


class Oferta(Base):
    __tablename__ = "oferta"

    id: Mapped[int] = mapped_column(primary_key=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("cliente.id"))
    monto: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    plazo_meses: Mapped[int]
    tea: Mapped[Decimal] = mapped_column(Numeric(6, 4))
    comision: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    estado: Mapped[str] = mapped_column(String(20), default="pendiente")
    creada_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=ahora_utc)


class ConsultaBuro(Base):
    """Cada fila es una consulta que el buró nos cobró."""

    __tablename__ = "consulta_buro"

    id: Mapped[int] = mapped_column(primary_key=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("cliente.id"))
    score: Mapped[int]
    creada_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=ahora_utc)


class EventoOutbox(Base):
    """Eventos pendientes de enviar a la plataforma de marketing."""

    __tablename__ = "evento_outbox"

    id: Mapped[int] = mapped_column(primary_key=True)
    tipo: Mapped[str] = mapped_column(String(50))
    cliente_id: Mapped[int] = mapped_column(ForeignKey("cliente.id"))
    payload: Mapped[dict] = mapped_column(JSON)
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=ahora_utc)
    enviado_en: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
