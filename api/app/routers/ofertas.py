from datetime import date
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.atraso import dias_de_atraso
from app.auth import cliente_actual
from app.config import SCORE_MINIMO, TEA_POR_PLAZO
from app.cronograma import generar_cronograma
from app.db import get_db
from app.models import Cliente, Oferta
from app.schemas import CuotaOut, OfertaIn, OfertaOut
from app.servicios import calcular_comision, obtener_score

router = APIRouter()


@router.post("/ofertas", response_model=OfertaOut, status_code=201)
def crear_oferta(
    datos: OfertaIn,
    cliente: Cliente = Depends(cliente_actual),
    db: Session = Depends(get_db),
):
    if datos.plazo_meses not in TEA_POR_PLAZO:
        raise HTTPException(status_code=422, detail="plazo_invalido")
    if obtener_score(db, cliente) < SCORE_MINIMO:
        raise HTTPException(status_code=422, detail="score_insuficiente")

    monto = Decimal(str(datos.monto))
    oferta = Oferta(
        cliente_id=cliente.id,
        monto=monto,
        plazo_meses=datos.plazo_meses,
        tea=TEA_POR_PLAZO[datos.plazo_meses],
        comision=calcular_comision(monto),
    )
    db.add(oferta)
    db.commit()
    return oferta


@router.get("/ofertas", response_model=list[OfertaOut])
def mis_ofertas(cliente: Cliente = Depends(cliente_actual), db: Session = Depends(get_db)):
    return db.scalars(
        select(Oferta).where(Oferta.cliente_id == cliente.id).order_by(Oferta.id)
    ).all()


@router.get("/ofertas/{oferta_id}", response_model=OfertaOut)
def ver_oferta(
    oferta_id: int,
    cliente: Cliente = Depends(cliente_actual),
    db: Session = Depends(get_db),
):
    oferta = db.get(Oferta, oferta_id)
    if oferta is None:
        raise HTTPException(status_code=404, detail="oferta_inexistente")
    return oferta


@router.get("/ofertas/{oferta_id}/cronograma", response_model=list[CuotaOut])
def cronograma(
    oferta_id: int,
    primer_vencimiento: date,
    cliente: Cliente = Depends(cliente_actual),
    db: Session = Depends(get_db),
):
    oferta = ver_oferta(oferta_id, cliente, db)
    cuotas = generar_cronograma(
        oferta.monto, oferta.tea, oferta.plazo_meses, primer_vencimiento
    )
    return [
        CuotaOut(**vars(c), dias_de_atraso=dias_de_atraso(c.vencimiento)) for c in cuotas
    ]
