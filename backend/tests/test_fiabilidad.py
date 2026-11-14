from backend.app.db import fiabilidad_por_id, todos_los_vehiculos
from backend.app.services.puntaje import etiqueta_fiabilidad, puntaje_fiabilidad


def test_captiva_turbo_fiabilidad_baja():
    """Regla obligatoria: toda Captiva 1.5 turbo tiene puntaje ≤ 4,0 y alerta ROJA."""
    captivas = [v for v in todos_los_vehiculos() if v["marca"] == "Chevrolet" and v["modelo"] == "Captiva"
                and "1.5" in v["motor_descripcion"] and v["alimentacion"] == "Turbo"]
    assert captivas, "El catálogo debe incluir la Captiva 1.5 Turbo"
    for v in captivas:
        f = fiabilidad_por_id()[v["id"]]
        assert f["puntaje_fiabilidad"] <= 4.0, v["slug"]
        assert any(a["nivel"] == "ROJA" for a in f["alertas"]), v["slug"]
        textos = " ".join(x["descripcion"].lower() for x in f["fallas_comunes_y_contras"])
        for palabra in ("cvt", "consumo", "pequeño", "depreciación"):
            assert palabra in textos or palabra in f["veredicto_honesto"].lower(), (v["slug"], palabra)
        for falla in f["fallas_comunes_y_contras"]:
            if falla["tipo"] == "documentada":
                assert len(falla["fuentes_ids"]) >= 2


def test_formula_publicada():
    d = {"motor_transmision": 10, "electrica_electronica": 10, "quejas_documentadas": 10, "recalls": 10,
         "repuestos_y_red": 10, "costo_reparaciones": 10}
    assert puntaje_fiabilidad(d) == 10.0
    d2 = {**d, "motor_transmision": 0}
    assert puntaje_fiabilidad(d2) == 6.5


def test_alerta_roja_limita_puntaje():
    d = {k: 9 for k in ("motor_transmision", "electrica_electronica", "quejas_documentadas", "recalls",
                        "repuestos_y_red", "costo_reparaciones")}
    assert puntaje_fiabilidad(d, [{"nivel": "ROJA", "texto": "x"}]) == 4.0
    assert puntaje_fiabilidad(d, [{"nivel": "AMARILLA", "texto": "x"}]) == 9.0


def test_etiquetas():
    assert etiqueta_fiabilidad(9.0) == "Excelente"
    assert etiqueta_fiabilidad(3.9) == "Crítica"


def test_cada_resena_tiene_pros_y_contras():
    for f in fiabilidad_por_id().values():
        assert len(f["pros_reales"]) >= 3
        assert len(f["fallas_comunes_y_contras"]) >= 2
        assert 350 <= len(f["veredicto_honesto"]) <= 700
