from tests.conftest import ANA, BRUNO


def test_crear_oferta(api):
    r = api.post("/ofertas", json={"monto": 10000, "plazo_meses": 6}, headers=ANA)
    assert r.status_code == 201
    oferta = r.json()
    assert oferta["tea"] == 0.75
    assert oferta["comision"] == 200
    assert oferta["estado"] == "pendiente"


def test_score_insuficiente(api):
    r = api.post("/ofertas", json={"monto": 10000, "plazo_meses": 6}, headers=BRUNO)
    assert r.status_code == 422
    assert r.json()["detail"] == "score_insuficiente"


def test_plazo_invalido(api):
    r = api.post("/ofertas", json={"monto": 10000, "plazo_meses": 5}, headers=ANA)
    assert r.status_code == 422
