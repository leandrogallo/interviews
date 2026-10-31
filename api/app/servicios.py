import logging
from decimal import Decimal

from sqlalchemy.orm import Session

from app.buro_falso import buro
from app.config import COMISION_ADMINISTRATIVA
from app.models import Cliente, ConsultaBuro, EventoOutbox

logger = logging.getLogger(__name__)


def obtener_score(db: Session, cliente: Cliente) -> int:
    logger.info("Consultando el buró para la cédula %s", cliente.cedula)
    score = buro.consultar(cliente.cedula)
    db.add(ConsultaBuro(cliente_id=cliente.id, score=score))
    db.commit()
    return score


def calcular_comision(monto: Decimal) -> Decimal:
    return Decimal(int(monto * COMISION_ADMINISTRATIVA))


def registrar_conversion(db: Session, cliente: Cliente) -> None:
    """Deja en el outbox el evento «Lead» para la plataforma de marketing.

    Un proceso aparte (fuera de esta prueba) lee el outbox y lo envía.
    """
    db.add(
        EventoOutbox(
            tipo="Lead",
            cliente_id=cliente.id,
            payload={"email": cliente.email, "cedula": cliente.cedula},
        )
    )
    db.commit()
