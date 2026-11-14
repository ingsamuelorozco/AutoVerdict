from backend.app.services import altura, indices
from backend.app.services.comparador import _ganadores


def test_ganador_max_min_y_empate():
    vs = [{}, {}, {}]
    assert _ganadores([100, 200, 200], "max", vs)[0] == [1, 2]
    assert _ganadores([100, 200, 50], "min", vs)[0] == [2]


def test_nulos_no_participan_y_menos_de_dos():
    vs = [{}, {}, {}]
    assert _ganadores([None, 5, None], "max", vs)[0] == []
    assert _ganadores([None, 5, 7], "max", vs)[0] == [2]


def test_filas_informativas_sin_ganador():
    assert _ganadores([4000, 4500], "info", [{}, {}])[0] == []


def test_categorica_por_ranking():
    assert _ganadores(["Tambor", "Disco"], "cat:frenos_traseros", [{}, {}])[0] == [1]
    assert _ganadores(["Cable", "Inalámbrico", "No"], "cat:apple_carplay_android_auto", [{}, {}, {}])[0] == [1]


def test_autonomia_ciclos_distintos():
    vs = [{"autonomia_ciclo": "WLTP"}, {"autonomia_ciclo": "NEDC"}]
    gan, aviso = _ganadores([400, 500], "autonomia", vs)
    assert gan == [] and "ciclos distintos" in aviso


def test_diametro_rueda():
    assert indices.diametro_rueda_mm("215/55 R18") == round(18 * 25.4 + 2 * 215 * 0.55)
    assert indices.diametro_rueda_mm(None) is None


def test_rompemuelle_umbrales():
    assert indices.rompemuelle(210)["etiqueta"] == "Pasa sin problema"
    assert indices.rompemuelle(180)["etiqueta"] == "Pasa con cuidado"
    assert indices.rompemuelle(155)["etiqueta"] == "Precaución: entra en diagonal y despacio"
    assert indices.rompemuelle(130)["etiqueta"] == "Riesgo de raspar"


def test_garaje_niveles():
    assert indices.garaje(4500, 1990, 1800)["etiqueta"] == "Holgado"
    assert indices.garaje(4700, 2100, 1900)["etiqueta"] == "Justo"
    assert indices.garaje(5300, 2100, 1900)["etiqueta"] == "No cabe"
    assert indices.garaje(4500, 1990, 1800)["espacio_lateral_por_lado_mm"] == 300


def test_altura_bev_no_pierde():
    assert altura.potencia_efectiva(200, "Eléctrico", "100% Eléctrico BEV", 2600)["perdida_pct"] == 0
    atm = altura.potencia_efectiva(100, "Atmosférico", "Gasolina Corriente", 2600)
    turbo = altura.potencia_efectiva(100, "Turbo", "Gasolina Corriente", 2600)
    assert atm["potencia_efectiva_hp"] < turbo["potencia_efectiva_hp"] < 100
