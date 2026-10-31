from datetime import date, datetime, timezone


def dias_de_atraso(vencimiento: date, ahora: datetime | None = None) -> int:
    """Días de atraso de una cuota impaga que vence en `vencimiento`.

    Una cuota que vence hoy todavía no está atrasada.
    """
    ahora = ahora or datetime.now(timezone.utc)
    return max(0, (ahora.date() - vencimiento).days)
