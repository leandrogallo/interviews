from datetime import date, datetime, timezone

from app.atraso import dias_de_atraso


def test_dos_dias_despues():
    ahora = datetime(2026, 3, 12, 15, 0, tzinfo=timezone.utc)
    assert dias_de_atraso(date(2026, 3, 10), ahora) == 2


def test_el_dia_del_vencimiento_a_la_noche_no_esta_atrasada():
    # 01:30 UTC del 11 son las 22:30 del 10 en Montevideo.
    ahora = datetime(2026, 3, 11, 1, 30, tzinfo=timezone.utc)
    assert dias_de_atraso(date(2026, 3, 10), ahora) == 0
