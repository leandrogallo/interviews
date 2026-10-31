import os
from decimal import Decimal
from zoneinfo import ZoneInfo

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql+psycopg://credito:credito@localhost:5432/mini_credito"
)

# Monto máximo por plazo, en pesos.
TOPES_POR_PLAZO = {3: Decimal("20000"), 6: Decimal("40000"), 12: Decimal("60000")}

# Tasa efectiva anual por plazo.
TEA_POR_PLAZO = {3: Decimal("0.80"), 6: Decimal("0.75"), 12: Decimal("0.70")}

# Comisión administrativa: 2 % del monto, redondeada al centavo.
COMISION_ADMINISTRATIVA = Decimal("0.02")

# Score mínimo del buró para poder pedir un préstamo.
SCORE_MINIMO = 500

# Una consulta al buró sirve durante estos días.
DIAS_VALIDEZ_BURO = 30

# La empresa opera en Uruguay: los vencimientos son en hora de Montevideo.
ZONA_HORARIA = ZoneInfo("America/Montevideo")
