"""Autenticación simulada: el front manda el id del cliente en `X-Cliente-Id`.

En la vida real sería un JWT. Para esta prueba alcanza: tratalo como si el
header viniera de un token ya validado.
"""

from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Cliente


def cliente_actual(
    x_cliente_id: int = Header(...), db: Session = Depends(get_db)
) -> Cliente:
    cliente = db.get(Cliente, x_cliente_id)
    if cliente is None:
        raise HTTPException(status_code=401, detail="cliente_desconocido")
    return cliente
