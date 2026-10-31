from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass
class Cuota:
    numero: int
    vencimiento: date
    capital: Decimal
    interes: Decimal
    total: Decimal


def generar_cronograma(
    monto: Decimal, tea: Decimal, plazo_meses: int, primer_vencimiento: date
) -> list[Cuota]:
    """Cronograma de cuotas por sistema francés. Las reglas están en el README."""
    raise NotImplementedError
