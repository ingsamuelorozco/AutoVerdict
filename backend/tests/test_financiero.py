import pytest

from backend.app.services import financiero, reventa, seguro, tco
from backend.app.services.config import cfg


def test_soat_familiar_menor_1500():
    s = financiero.soat(1496, "Sedán", "Gasolina Corriente", 0)
    assert s["total_cop"] == cfg("tarifas_soat")["clases"]["familiar"]["rangos"][0]["menor_10"]


def test_soat_camioneta_y_antiguedad():
    nuevo = financiero.soat(2755, "Pickup", "Diésel", 0)["total_cop"]
    viejo = financiero.soat(2755, "Pickup", "Diésel", 12)["total_cop"]
    assert nuevo == 1110300 and viejo == 1274000


def test_soat_bev_con_descuento():
    bev = financiero.soat(None, "SUV", "100% Eléctrico BEV", 0)
    base = cfg("tarifas_soat")["clases"]["campero_camioneta"]["rangos"][0]["menor_10"]
    assert bev["total_cop"] < base
    assert bev["descuento_bev_cop"] > 0


def test_desglose_soat_suma_total():
    s = financiero.soat(1998, "SUV", "Gasolina Corriente", 0)
    assert abs(s["prima_cop"] + s["contribucion_adres_cop"] + s["tasa_runt_cop"] - s["total_cop"]) <= 2


def test_impuesto_bev_tope_1pct():
    i = financiero.impuesto_anual(200_000_000, "100% Eléctrico BEV", "medellin", 6)
    assert i["tarifa"] <= 0.01


def test_puesta_en_calle_identidad():
    p = financiero.puesta_en_calle(100_000_000, 1496, "Sedán", "Gasolina Corriente", "bogota", 11)
    assert p["total_cop"] == 100_000_000 + p["soat"]["total_cop"] + p["matricula"]["total_cop"]
    assert p["matricula"]["meses_restantes"] == 2


def test_cuota_formula_francesa():
    i = financiero.tasa_mensual(0.12)
    assert i == pytest.approx((1.12) ** (1 / 12) - 1)
    cuota = financiero.cuota_fija(10_000_000, i, 12)
    assert cuota == pytest.approx(10_000_000 * i / (1 - (1 + i) ** -12))


def test_credito_amortiza_todo():
    r = financiero.credito(100_000_000, cuota_inicial_pct=0.3, plazo_meses=60, tasa_ea=0.155, seguro_vida_mensual_pct=0)
    assert r["tabla"][-1]["saldo_cop"] == 0
    assert r["capital_financiado_cop"] == 70_000_000
    assert r["total_intereses_cop"] > 0


def test_abonos_reducen_intereses():
    sin = financiero.credito(100_000_000, plazo_meses=60, incluir_tabla=False)
    con = financiero.credito(100_000_000, plazo_meses=60, abonos=[{"mes": 6, "valor": 10_000_000}], incluir_tabla=False)
    assert con["total_intereses_cop"] < sin["total_intereses_cop"]
    assert con["meses_efectivos"] < 60
    cuota = financiero.credito(100_000_000, plazo_meses=60, abonos=[{"mes": 6, "valor": 10_000_000}], modo_abono="cuota")
    assert cuota["meses_efectivos"] == 60
    assert cuota["tabla"][10]["cuota_cop"] < cuota["tabla"][0]["cuota_cop"]


def test_cuota_balon_menor():
    fija = financiero.credito(100_000_000, plazo_meses=48, incluir_tabla=False)
    balon = financiero.credito(100_000_000, plazo_meses=48, tipo_cuota="balon", valor_final_pct=0.3, incluir_tabla=False)
    assert balon["cuota_mensual_cop"] < fija["cuota_mensual_cop"]


def test_alerta_usura():
    assert financiero.credito(50_000_000, tasa_ea=0.40, incluir_tabla=False)["supera_usura"]


def test_seguro_rango():
    s = seguro.todo_riesgo(100_000_000, "SUV Compacta", "bogota")
    assert s["prima_anual_min_cop"] < s["prima_anual_central_cop"] < s["prima_anual_max_cop"]
    joven = seguro.todo_riesgo(100_000_000, "SUV Compacta", "bogota", edad_conductor="18-25")
    assert joven["prima_anual_central_cop"] > s["prima_anual_central_cop"]


def test_reventa_monotona():
    c = reventa.curva_reventa(100_000_000, None, "Media")
    valores = [p["valor_cop"] for p in c["puntos"]]
    assert valores == sorted(valores, reverse=True)


def test_pico_y_placa_bogota_paridad():
    from datetime import date
    r = tco.pico_y_placa("Gasolina Corriente", "bogota", 6, date(2026, 11, 12))
    assert r["restringido_hoy"] is True
    assert tco.pico_y_placa("100% Eléctrico BEV", "bogota")["exento"] is True


def test_usado_soat_por_antiguedad_y_sin_alistamiento():
    from datetime import date
    from backend.app.services import financiero
    assert financiero.antiguedad_compra(2026, date(2026, 11, 1)) == 0
    assert financiero.antiguedad_compra(2024, "2025-03-01") == 0  # precio de vitrina del año siguiente
    assert financiero.antiguedad_compra(2010, "2026-11-01") == 16
    nuevo = financiero.puesta_en_calle(30_000_000, 1600, "Sedán", "Gasolina Corriente", "bogota", 11)
    usado = financiero.puesta_en_calle(30_000_000, 1600, "Sedán", "Gasolina Corriente", "bogota", 11, antiguedad_anios=16)
    assert usado["usado"] and not nuevo["usado"]
    assert usado["matricula"]["alistamiento_cop"] == 0
    assert usado["soat"]["total_cop"] >= nuevo["soat"]["total_cop"]
