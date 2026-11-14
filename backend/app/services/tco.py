"""Costo total de propiedad (TCO), combustible, pico y placa y punto de equilibrio."""
from __future__ import annotations

import math
from datetime import date
from typing import Any

from . import financiero, reventa, seguro
from .config import BEV, PHEV, cfg, ciudad


def costo_energia_por_km(v: dict[str, Any], ciudad_id: str | None, mezcla_ciudad: float | None = None,
                         carga_casa_pct: float | None = None, usar_real: bool = True) -> dict[str, Any]:
    comb = cfg("combustibles")
    cd = ciudad(ciudad_id)
    precios = cd["combustible"]
    casa = comb["carga_casa_pct_defecto"] if carga_casa_pct is None else carga_casa_pct
    kwh_precio = casa * precios["kwh_casa"] + (1 - casa) * precios["kwh_publico"]
    tipo = v["tipo_combustible"]
    mezcla = comb["mezcla_ciudad_defecto"] if mezcla_ciudad is None else mezcla_ciudad

    def kml() -> float | None:
        if usar_real and v.get("consumo_real_estimado_kml"):
            return v["consumo_real_estimado_kml"]
        ciu, car = v.get("consumo_ciudad_kml"), v.get("consumo_carretera_kml")
        if ciu and car:
            return 1 / (mezcla / ciu + (1 - mezcla) / car)
        return v.get("consumo_mixto_kml")

    galon = comb["litros_por_galon"]
    costo_elec = (v.get("consumo_kwh_100km") or 0) / 100 * kwh_precio
    if tipo == BEV:
        por_km = costo_elec
        detalle = {"fuente_energia": "electricidad", "precio_kwh_cop": round(kwh_precio)}
    else:
        clave = comb["combustible_por_tipo"].get(tipo, "corriente")
        if (v.get("octanaje_minimo_recomendado") or 0) >= comb["octanaje_extra_ron"]:
            clave = "extra"
        precio_galon = precios[clave]
        rend = kml()
        por_km_comb = (precio_galon / galon) / rend if rend else 0
        if tipo == PHEV and v.get("consumo_kwh_100km"):
            f = comb["phev_fraccion_electrica_defecto"]
            por_km = f * costo_elec + (1 - f) * por_km_comb
        else:
            por_km = por_km_comb
        detalle = {"fuente_energia": clave, "precio_galon_cop": precio_galon,
                   "rendimiento_kml": round(rend, 1) if rend else None}
    return {"costo_por_km_cop": por_km, "costo_1000km_cop": round(por_km * 1000), **detalle}


def pico_y_placa(tipo_combustible: str, ciudad_id: str | None, digito: int | None = None,
                 fecha: date | None = None) -> dict[str, Any]:
    cd = ciudad(ciudad_id)
    pp = cd["pico_placa"]
    exento = tipo_combustible in pp.get("exentos", [])
    res = {"ciudad": cd["nombre"], "regla": pp["descripcion"], "exento": exento,
           "nota_exencion": pp.get("nota_exencion"), "estado": pp["estado"], "fuente_url": pp.get("fuente_url"),
           "aviso": "Verifica la norma vigente de tu ciudad."}
    if digito is not None and not exento:
        f = fecha or date.today()
        restringido = False
        if pp["regla"] == "paridad_dia":
            restringido = digito in (pp["pares"] if f.day % 2 == 0 else pp["impares"])
        elif pp["regla"] == "dia_semana":
            dias = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
            restringido = digito in pp.get("dias", {}).get(dias[f.weekday()], [])
        res.update({"digito": digito, "fecha": f.isoformat(), "restringido_hoy": restringido and f.weekday() < 5})
    return res


def mantenimiento_anual(nivel: str, km_anio: float, tipo_combustible: str, costo_modelo: float | None = None) -> float:
    m = cfg("mantenimiento")
    hito = m["costo_hito_10000km_cop"].get(nivel, m["costo_hito_10000km_cop"]["Moderado"])
    if costo_modelo:
        return costo_modelo * km_anio / cfg("combustibles")["km_anuales_defecto"]
    factor = m["factor_bev"] if tipo_combustible == BEV else 1.0
    return hito * km_anio / 10000 * factor


def costo_mantenimiento_km(nivel: str, km: float, tipo_combustible: str) -> float:
    """Costo acumulado por hitos de 10.000 km, con hitos mayores periódicos."""
    m = cfg("mantenimiento")
    hito = m["costo_hito_10000km_cop"].get(nivel, m["costo_hito_10000km_cop"]["Moderado"])
    factor = m["factor_bev"] if tipo_combustible == BEV else 1.0
    total = 0.0
    for k in range(10000, int(km) + 1, 10000):
        mult = m["multiplicador_hito_mayor"] if k % m["hitos_mayores_cada_km"] == 0 else 1.0
        total += hito * mult
    return total * factor


def tco(v: dict[str, Any], anios: int = 5, km_anio: float | None = None, mezcla_ciudad: float | None = None,
        ciudad_id: str | None = None, carga_casa_pct: float | None = None, financiar: bool = False,
        credito_params: dict[str, Any] | None = None, seguro_params: dict[str, Any] | None = None) -> dict[str, Any]:
    comb = cfg("combustibles")
    mant_cfg = cfg("mantenimiento")
    km = km_anio or comb["km_anuales_defecto"]
    anios = max(1, min(10, int(anios)))
    precio = v["precio_base_cop"]
    pec = financiero.puesta_en_calle(precio, v.get("cilindraje_cc"), v["carroceria"], v["tipo_combustible"], ciudad_id)
    energia = costo_energia_por_km(v, ciudad_id, mezcla_ciudad, carga_casa_pct)
    curva = reventa.retencion_completa(v.get("retencion_valor"), v.get("depreciacion_estimada"))
    sp = seguro_params or {}
    comp = {k: 0.0 for k in ("combustible", "mantenimiento", "seguro", "soat", "impuesto", "tecnomecanica", "intereses")}
    por_anio = []
    for a in range(1, anios + 1):
        avaluo_a = financiero.avaluo_estimado(precio) * reventa.interpolar(curva, a - 1)
        fila = {
            "combustible": energia["costo_por_km_cop"] * km,
            "mantenimiento": mantenimiento_anual(v.get("nivel_costo_mantenimiento") or "Moderado", km, v["tipo_combustible"]),
            "seguro": seguro.todo_riesgo(avaluo_a, v.get("segmento", ""), ciudad_id, antiguedad_anios=a - 1,
                                         riesgo_hurto=v.get("riesgo_hurto") or "Medio",
                                         tipo_combustible=v["tipo_combustible"], **sp)["prima_anual_central_cop"],
            "soat": pec["soat"]["total_cop"] if a == 1 else financiero.soat(v.get("cilindraje_cc"), v["carroceria"], v["tipo_combustible"], a - 1)["total_cop"],
            "impuesto": pec["matricula"]["impuesto_proporcional_cop"] if a == 1 else financiero.impuesto_anual(avaluo_a, v["tipo_combustible"], ciudad_id, a - 1)["valor_anual_cop"],
            "tecnomecanica": 0.0,
        }
        if a >= mant_cfg["revision_tecnomecanica_desde_anio"]:
            desc = mant_cfg["revision_tecnomecanica_descuento_bev"] if v["tipo_combustible"] == BEV else 0
            fila["tecnomecanica"] = mant_cfg["revision_tecnomecanica_cop"] * (1 - desc)
        for k, val in fila.items():
            comp[k] += val
        por_anio.append({"anio": a, **{k: round(val) for k, val in fila.items()}})
    if financiar:
        cr = financiero.credito(precio, incluir_tabla=False, plazo_meses=min(anios * 12, cfg("credito")["plazo_max_meses"]),
                                **(credito_params or {}))
        comp["intereses"] = cr["total_intereses_cop"] + cr["total_seguros_cop"]
    valor_reventa = precio * reventa.interpolar(curva, anios)
    tramites = pec["matricula"]["total_cop"]
    costo_bruto = sum(comp.values()) + tramites
    neto = precio + costo_bruto - valor_reventa
    meses = anios * 12
    return {
        "anios": anios, "km_anio": km, "componentes_cop": {k: round(v_) for k, v_ in comp.items()},
        "tramites_iniciales_cop": tramites, "precio_base_cop": precio,
        "valor_reventa_cop": round(valor_reventa, -3),
        "depreciacion_cop": round(precio - valor_reventa, -3),
        "costo_total_neto_cop": round(neto, -3),
        "costo_operativo_cop": round(neto - (precio - valor_reventa), -3),
        "costo_por_mes_cop": round(neto / meses, -3),
        "costo_por_km_cop": round(neto / (km * anios)),
        "por_anio": por_anio, "energia": energia, "estado": "estimado",
    }


def punto_equilibrio(v_electrificado: dict[str, Any], v_gasolina: dict[str, Any], ciudad_id: str | None = None,
                     km_anio: float | None = None, carga_casa_pct: float | None = None) -> dict[str, Any]:
    km = km_anio or cfg("combustibles")["km_anuales_defecto"]
    e1 = costo_energia_por_km(v_electrificado, ciudad_id, carga_casa_pct=carga_casa_pct)["costo_por_km_cop"]
    e2 = costo_energia_por_km(v_gasolina, ciudad_id)["costo_por_km_cop"]
    m1 = mantenimiento_anual(v_electrificado.get("nivel_costo_mantenimiento") or "Moderado", km, v_electrificado["tipo_combustible"])
    m2 = mantenimiento_anual(v_gasolina.get("nivel_costo_mantenimiento") or "Moderado", km, v_gasolina["tipo_combustible"])
    ahorro_anual = (e2 - e1) * km + (m2 - m1)
    diferencia = v_electrificado["precio_base_cop"] - v_gasolina["precio_base_cop"]
    if diferencia <= 0:
        anios = 0.0
    elif ahorro_anual <= 0:
        anios = math.inf
    else:
        anios = diferencia / ahorro_anual
    return {
        "diferencia_precio_cop": round(diferencia), "ahorro_anual_cop": round(ahorro_anual),
        "anios_equilibrio": None if math.isinf(anios) else round(anios, 1),
        "km_equilibrio": None if math.isinf(anios) else round(anios * km, -2),
        "estado": "estimado",
    }
