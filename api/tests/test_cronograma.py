from datetime import date
from decimal import Decimal

from app.cronograma import generar_cronograma


def test_el_capital_suma_el_monto():
    cuotas = generar_cronograma(Decimal("10000"), Decimal("0.75"), 6, date(2026, 3, 10))
    assert len(cuotas) == 6
    assert sum(c.capital for c in cuotas) == Decimal("10000")
