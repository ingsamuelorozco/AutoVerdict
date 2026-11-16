def test_salud(client):
    r = client.get("/api/salud")
    assert r.status_code == 200 and r.json()["vehiculos"] >= 300


def test_cascada(client):
    marcas = client.get("/api/catalogo/marcas").json()
    assert len(marcas) >= 18
    modelos = client.get("/api/catalogo/modelos", params={"marca": "Mazda"}).json()
    anios = client.get("/api/catalogo/anios", params={"marca": "Mazda", "modelo": modelos[0]["modelo"]}).json()
    vers = client.get("/api/catalogo/versiones", params={"marca": "Mazda", "modelo": modelos[0]["modelo"], "anio": anios[0]}).json()
    assert vers and "id" in vers[0]


def test_busqueda_tolerante_a_tildes(client):
    a = client.get("/api/vehiculos", params={"q": "captiva"}).json()["total"]
    b = client.get("/api/vehiculos", params={"q": "Captivá"}).json()["total"]
    assert a == b > 0


def test_busqueda_sin_resultados_sugiere(client):
    r = client.get("/api/vehiculos", params={"baul_min": 99999}).json()
    assert r["total"] == 0 and r["sugerencia"]


def test_ficha_por_slug(client):
    v = client.get("/api/vehiculos", params={"size": 1}).json()["resultados"][0]
    f = client.get(f"/api/vehiculos/{v['slug']}", params={"ciudad": "cali"}).json()
    for seccion in ("especificaciones", "tamano", "precio", "costo", "fiabilidad", "rivales"):
        assert seccion in f
    pec = f["precio"]["puesta_en_calle"]
    assert pec["total_cop"] == pec["precio_base_cop"] + pec["soat"]["total_cop"] + pec["matricula"]["total_cop"]


def test_comparar_y_marcador(client):
    ids = [v["id"] for v in client.get("/api/vehiculos", params={"size": 3}).json()["resultados"]]
    r = client.post("/api/comparar", json={"ids": ids, "perfil": "ciudad"})
    assert r.status_code == 200
    d = r.json()
    assert len(d["puntajes"]) == 3 and all(0 <= p["puntaje"] <= 100 for p in d["puntajes"])
    assert sum(m["total"] for m in d["marcador"].values()) > 0


def test_comparar_limites(client):
    assert client.post("/api/comparar", json={"ids": [1]}).status_code == 422
    assert client.post("/api/comparar", json={"ids": list(range(1, 12))}).status_code == 422


def test_error_formato_unico(client):
    r = client.get("/api/vehiculos/no-existe")
    assert r.status_code == 404
    assert set(r.json()) == {"codigo", "mensaje", "detalle"}


def test_etag(client):
    r = client.get("/api/catalogo/marcas")
    assert "etag" in r.headers and "cache-control" in r.headers
    assert client.get("/api/catalogo/marcas", headers={"If-None-Match": r.headers["etag"]}).status_code == 304


def test_alertas_rojas_en_buscador(client):
    r = client.get("/api/fiabilidad", params={"solo_alertas_rojas": "true"}).json()
    assert any(x["modelo"] == "Captiva" for x in r["resultados"])


def test_resena_con_checklist(client):
    slug = client.get("/api/fiabilidad", params={"q": "fiesta"}).json()["resultados"][0]["slug"]
    r = client.get(f"/api/fiabilidad/{slug}").json()
    assert r["checklist_usado"] and r["desglose"] and r["aviso_legal"]


def test_herramientas(client):
    assert client.post("/api/financiero/credito", json={"precio_cop": 90000000}).json()["escenarios"]
    assert client.post("/api/financiero/asequibilidad", json={"ingreso_mensual_cop": 8000000, "cuota_inicial_cop": 20000000}).status_code == 200
    assert client.post("/api/financiero/puesta-en-calle", json={}).status_code == 422


def test_modelos_agrupa_versiones_y_separa_carrocerias(client):
    r = client.get("/api/vehiculos/modelos", params={"marca": "Mazda", "size": 100}).json()
    nombres = [m["modelo"] for m in r["resultados"]]
    assert len(nombres) == len(set(nombres)), "cada modelo aparece una sola vez"
    assert {"2 Sedán", "2 Hatchback"} <= set(nombres), "sedán y hatchback siguen separados"
    sedan = next(m for m in r["resultados"] if m["modelo"] == "2 Sedán")
    assert sedan["versiones"] > 1 and sedan["anios"] == sorted(sedan["anios"], reverse=True)
    assert r["total_versiones"] == client.get("/api/vehiculos", params={"marca": "Mazda"}).json()["total"]


def test_modelos_respeta_filtros(client):
    r = client.get("/api/vehiculos/modelos", params={"q": "captiva"}).json()
    assert r["total"] == 1 and r["resultados"][0]["tiene_alerta_roja"]
    assert client.get("/api/vehiculos/modelos", params={"baul_min": 99999}).json()["sugerencia"]


def test_filtro_por_modelo(client):
    vs = client.get("/api/vehiculos", params={"marca": "Mazda", "modelo": "2 Sedán", "size": 100}).json()["resultados"]
    assert vs and all(v["modelo"] == "2 Sedán" for v in vs)
