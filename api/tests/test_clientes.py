from tests.conftest import ANA, BRUNO


def test_ana_es_elegible(api):
    r = api.get("/clientes/yo/elegibilidad", headers=ANA)
    assert r.status_code == 200
    assert r.json() == {"elegible": True, "score": 820}


def test_bruno_no_es_elegible(api):
    r = api.get("/clientes/yo/elegibilidad", headers=BRUNO)
    assert r.json()["elegible"] is False


def test_sin_cliente_da_401(api):
    assert api.get("/clientes/yo/elegibilidad", headers={"X-Cliente-Id": "99"}).status_code == 401
