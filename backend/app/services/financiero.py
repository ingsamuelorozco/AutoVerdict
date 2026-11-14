"""Motor financiero colombiano: SOAT, matrícula, impuesto, puesta en calle, crédito y asequibilidad."""
from __future__ import annotations

from datetime import date
from typing import Any

from .config import BEV, HEV, PHEV, cfg, ciudad, meta


# ---------------------------------------------------------------- SOAT
def soat(cilindraje_cc: int | None, carroceria: str, tipo_combustible: str, antiguedad_anios: int = 0) -> dict[str, Any]:
    c = cfg("tarifas_soat")
    clase_id = c["clase_por_carroceria"].get(carroceria, "familiar")
    clase = c["clases"][clase_id]
    cc = cilindraje_cc or 0
    rango = next(r for r in clase["rangos"] if r["cc_max"] is None or cc <= r["cc_max"])
    columna = "mayor_igual_10" if antiguedad_anios >= c["antiguedad_limite_anios"] else "menor_10"
    total_tabla = rango[columna]
    runt = c["tasa_runt_cop"]
    adres = c["contribucion_adres_pct"]
    prima = (total_tabla - runt) / (1 + adres)
    descuento = prima * c["descuento_bev_pct"] if tipo_combustible == BEV else 0.0
    prima_neta = prima - descuento
    contribucion = prima_neta * adres
    total = round(prima_neta + contribucion + runt)
    return {
        "clase": clase["etiqueta"],
        "rango_cc": f"hasta {rango['cc_max']} cc" if rango["cc_max"] else "más de 2.500 cc",
        "prima_cop": round(prima_neta),
        "contribucion_adres_cop": round(contribucion),
        "tasa_runt_cop": runt,
        "descuento_bev_cop": round(descuento * (1 + adres)),
        "total_cop": total,
        "estado_desglose": "estimado",
        "nota": c["nota_bev"] if tipo_combustible == BEV else c["nota"],
        **meta("tarifas_soat"),
    }


# ---------------------------------------------------------------- Impuesto vehicular
def avaluo_estimado(precio_base_cop: float) -> int:
    iva = cfg("matricula")["impuesto"]["iva_vehiculos"]
    return round(precio_base_cop / (1 + iva), -3)


def impuesto_anual(avaluo_cop: float, tipo_combustible: str, ciudad_id: str | None,
                   anios_desde_matricula: int = 0) -> dict[str, Any]:
    imp = cfg("matricula")["impuesto"]
    cd = ciudad(ciudad_id)
    rangos = cd.get("impuesto_rangos") or imp["rangos_nacionales"]
    tarifa = next(r["tarifa"] for r in rangos if r["hasta_cop"] is None or avaluo_cop <= r["hasta_cop"])
    descuento_pct = 0.0
    if tipo_combustible == BEV:
        tarifa = min(cd.get("impuesto_bev_tarifa") or tarifa, imp["tope_bev"])
        if anios_desde_matricula < 5:
            descuento_pct = cd.get("descuento_bev_pct") or 0
    elif tipo_combustible in (HEV, PHEV) and anios_desde_matricula < 5:
        descuento_pct = cd.get("descuento_hibrido_pct") or 0
    bruto = avaluo_cop * tarifa
    neto = bruto * (1 - descuento_pct)
    return {
        "avaluo_cop": round(avaluo_cop), "tarifa": tarifa, "descuento_pct": descuento_pct,
        "valor_anual_cop": round(neto), "fuente": imp["fuente"], "fuente_url": cd.get("fuente_impuesto") or imp["fuente_url"],
    }


def meses_restantes(mes_compra: int) -> int:
    return 12 - mes_compra + 1


# ---------------------------------------------------------------- Matrícula y puesta en calle
def matricula(precio_base_cop: float, tipo_combustible: str, ciudad_id: str | None,
              mes_compra: int | None = None, incluir_alistamiento: bool | None = None) -> dict[str, Any]:
    c = cfg("matricula")
    cd = ciudad(ciudad_id)
    mes = mes_compra or date.today().month
    avaluo = avaluo_estimado(precio_base_cop)
    imp = impuesto_anual(avaluo, tipo_combustible, cd["id"], 0)
    meses = meses_restantes(mes)
    impuesto_prop = round(imp["valor_anual_cop"] * meses / 12)
    alist_cfg = c["alistamiento"]
    alist_activo = alist_cfg["activo_por_defecto"] if incluir_alistamiento is None else incluir_alistamiento
    alistamiento = alist_cfg["valor_cop"] if alist_activo else 0
    derechos = cd["matricula_cop"]
    return {
        "ciudad": cd["nombre"],
        "derechos_matricula_placas_runt_cop": derechos,
        "estado_derechos": cd["estado_matricula"],
        "fuente_derechos": cd["fuente_matricula"],
        "impuesto_anual_cop": imp["valor_anual_cop"],
        "impuesto_tarifa": imp["tarifa"],
        "impuesto_descuento_pct": imp["descuento_pct"],
        "meses_restantes": meses,
        "impuesto_proporcional_cop": impuesto_prop,
        "avaluo_estimado_cop": avaluo,
        "alistamiento_cop": alistamiento,
        "total_cop": derechos + impuesto_prop + alistamiento,
        **meta("matricula"),
    }


def puesta_en_calle(precio_base_cop: float, cilindraje_cc: int | None, carroceria: str, tipo_combustible: str,
                    ciudad_id: str | None, mes_compra: int | None = None,
                    incluir_alistamiento: bool | None = None) -> dict[str, Any]:
    s = soat(cilindraje_cc, carroceria, tipo_combustible, 0)
    m = matricula(precio_base_cop, tipo_combustible, ciudad_id, mes_compra, incluir_alistamiento)
    total = round(precio_base_cop) + s["total_cop"] + m["total_cop"]
    return {"precio_base_cop": round(precio_base_cop), "soat": s, "matricula": m,
            "total_cop": total, "etiqueta_total": "Precio total puesto en calle (llave en mano)"}


# ---------------------------------------------------------------- Crédito
def tasa_mensual(tasa_ea: float) -> float:
    return (1 + tasa_ea) ** (1 / 12) - 1


def cuota_fija(capital: float, i: float, n: int, valor_final: float = 0.0) -> float:
    if n <= 0:
        return capital
    if i == 0:
        return (capital - valor_final) / n
    vp_final = valor_final / (1 + i) ** n
    return (capital - vp_final) * i / (1 - (1 + i) ** (-n))


def _amortizar(capital: float, i: float, n: int, valor_final: float, seguro_vida_pct: float,
               seguro_vehiculo_mensual: float, abonos: dict[int, float], modo_abono: str) -> dict[str, Any]:
    saldo = capital
    cuota = cuota_fija(capital, i, n, valor_final)
    tabla = []
    total_int = total_seg = 0.0
    mes = 0
    while saldo > 0.5 and mes < n:
        mes += 1
        interes = saldo * i
        seguro = saldo * seguro_vida_pct + seguro_vehiculo_mensual
        pago_capital = cuota - interes
        if mes == n:
            pago_capital = saldo
        pago_capital = min(pago_capital, saldo)
        abono = min(abonos.get(mes, 0.0), max(saldo - pago_capital, 0.0))
        saldo -= pago_capital + abono
        total_int += interes
        total_seg += seguro
        tabla.append({"mes": mes, "cuota_cop": round(pago_capital + interes), "interes_cop": round(interes),
                      "capital_cop": round(pago_capital), "abono_cop": round(abono), "seguros_cop": round(seguro),
                      "saldo_cop": round(max(saldo, 0)), "interes_acumulado_cop": round(total_int)})
        if abono and modo_abono == "cuota" and mes < n and saldo > 0.5:
            cuota = cuota_fija(saldo, i, n - mes, valor_final)
    return {"cuota_base": cuota_fija(capital, i, n, valor_final), "tabla": tabla,
            "total_intereses": total_int, "total_seguros": total_seg, "meses": mes}


def credito(precio_cop: float, tramites_cop: float = 0.0, financiar_tramites: bool = False,
            cuota_inicial_pct: float | None = None, cuota_inicial_cop: float | None = None,
            plazo_meses: int | None = None, tasa_ea: float | None = None,
            seguro_vida_mensual_pct: float | None = None, seguro_vehiculo_mensual_cop: float = 0.0,
            comision_cop: float | None = None, tipo_cuota: str = "fija", valor_final_pct: float = 0.0,
            abonos: list[dict[str, float]] | None = None, modo_abono: str = "plazo",
            max_pct_ingreso: float | None = None, incluir_tabla: bool = True) -> dict[str, Any]:
    c = cfg("credito")
    plazo = int(plazo_meses or c["plazo_defecto_meses"])
    plazo = max(c["plazo_min_meses"], min(c["plazo_max_meses"], plazo))
    ea = c["tasa_defecto_ea"] if tasa_ea is None else tasa_ea
    vida = c["seguro_vida_deudor_mensual_pct"] if seguro_vida_mensual_pct is None else seguro_vida_mensual_pct
    comision = c["comision_estudio_cop"] if comision_cop is None else comision_cop
    max_pct = max_pct_ingreso or c["max_pct_ingreso"]
    base = precio_cop + (tramites_cop if financiar_tramites else 0)
    if cuota_inicial_cop is not None:
        inicial = cuota_inicial_cop
    else:
        inicial = base * (c["cuota_inicial_pct_defecto"] if cuota_inicial_pct is None else cuota_inicial_pct)
    capital = max(base - inicial + comision, 0.0)
    i = tasa_mensual(ea)
    valor_final = precio_cop * valor_final_pct if tipo_cuota == "balon" else 0.0
    abonos_map = {int(a["mes"]): float(a["valor"]) for a in (abonos or [])}

    plan = _amortizar(capital, i, plazo, valor_final, vida, seguro_vehiculo_mensual_cop, abonos_map, modo_abono)
    sin_abonos = _amortizar(capital, i, plazo, valor_final, vida, seguro_vehiculo_mensual_cop, {}, modo_abono) if abonos_map else plan
    cuota_total_mes1 = plan["tabla"][0]["cuota_cop"] + plan["tabla"][0]["seguros_cop"] if plan["tabla"] else 0
    total_pagado = capital + plan["total_intereses"] + plan["total_seguros"]
    costo_credito = plan["total_intereses"] + plan["total_seguros"] + comision
    res = {
        "capital_financiado_cop": round(capital),
        "cuota_inicial_cop": round(inicial),
        "tasa_ea": ea, "tasa_mensual": round(i, 6), "plazo_meses": plazo,
        "cuota_mensual_cop": round(plan["cuota_base"]),
        "cuota_mensual_con_seguros_cop": round(cuota_total_mes1),
        "valor_final_cop": round(valor_final),
        "total_intereses_cop": round(plan["total_intereses"]),
        "total_seguros_cop": round(plan["total_seguros"]),
        "costo_total_credito_cop": round(costo_credito),
        "total_pagado_cop": round(total_pagado + inicial),
        "sobrecosto_pct": round(costo_credito / precio_cop, 4) if precio_cop else 0,
        "ingreso_minimo_recomendado_cop": round(cuota_total_mes1 / max_pct),
        "max_pct_ingreso": max_pct,
        "meses_efectivos": plan["meses"],
        "ahorro_intereses_por_abonos_cop": round(sin_abonos["total_intereses"] - plan["total_intereses"]),
        "supera_usura": ea > c["tasa_usura_ea"],
        "tasa_usura_ea": c["tasa_usura_ea"],
        "aviso": c["aviso"],
        **meta("credito"),
    }
    if incluir_tabla:
        res["tabla"] = plan["tabla"]
    return res


def escenarios_credito(precio_cop: float, **kw: Any) -> list[dict[str, Any]]:
    out = []
    for n in cfg("credito")["escenarios_meses"]:
        r = credito(precio_cop, plazo_meses=n, incluir_tabla=False, **{k: v for k, v in kw.items() if k != "plazo_meses"})
        out.append({k: r[k] for k in ("plazo_meses", "cuota_mensual_con_seguros_cop", "total_intereses_cop",
                                      "costo_total_credito_cop", "sobrecosto_pct")})
    return out
