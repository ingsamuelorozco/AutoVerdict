"""Índices dimensionales: Rompemuelle, Garaje, baúl en objetos y comodidad trasera."""
from __future__ import annotations

import math
import re
from typing import Any

from .config import cfg


def diametro_rueda_mm(medida_llantas: str | None) -> int | None:
    """'215/55 R18' -> diámetro exterior en mm."""
    if not medida_llantas:
        return None
    m = re.search(r"(\d{3})\s*/\s*(\d{2})\s*Z?R\s*(\d{2})", medida_llantas.upper())
    if not m:
        return None
    ancho, perfil, rin = int(m.group(1)), int(m.group(2)), int(m.group(3))
    return round(rin * 25.4 + 2 * ancho * perfil / 100)


def rompemuelle(despeje_mm: float | None, voladizo_delantero_mm: float | None = None,
                angulo_ventral_deg: float | None = None, carga: bool = False,
                tope_mm: float | None = None) -> dict[str, Any] | None:
    if despeje_mm is None:
        return None
    c = cfg("indices")["rompemuelle"]
    efectivo = float(despeje_mm)
    if voladizo_delantero_mm and voladizo_delantero_mm > c["voladizo_delantero_umbral_mm"]:
        exceso = voladizo_delantero_mm - c["voladizo_delantero_umbral_mm"]
        efectivo -= exceso / 100 * c["penalizacion_por_100mm_voladizo"]
    if angulo_ventral_deg is not None and angulo_ventral_deg < c["angulo_ventral_umbral_deg"]:
        efectivo -= c["penalizacion_angulo_ventral_mm"]
    con_carga = efectivo - c["caida_con_carga_mm"]
    base = con_carga if carga else efectivo
    nivel = next(n for n in c["niveles"] if base >= n["min_mm"])
    topes = []
    for t in ([tope_mm] if tope_mm else c["topes_simulables_mm"]):
        margen = con_carga - t
        estado = "Pasa" if margen >= c["margen_holgado_mm"] else ("Justo" if margen >= 0 else "Raspa")
        topes.append({"tope_mm": t, "margen_mm": round(margen), "estado": estado})
    return {
        "nivel": nivel["nivel"], "etiqueta": nivel["etiqueta"],
        "despeje_mm": despeje_mm, "despeje_efectivo_mm": round(efectivo),
        "despeje_con_carga_mm": round(con_carga), "topes": topes, "estado": "estimado",
    }


def garaje(largo_mm: float | None, ancho_con_espejos_mm: float | None, ancho_sin_espejos_mm: float | None,
           plaza_largo_mm: float | None = None, plaza_ancho_mm: float | None = None) -> dict[str, Any] | None:
    if not largo_mm or not ancho_con_espejos_mm:
        return None
    g = cfg("indices")["garaje"]
    pl = plaza_largo_mm or g["plaza_largo_mm"]
    pa = plaza_ancho_mm or g["plaza_ancho_mm"]
    # Los umbrales se escalan si el usuario cambia el tamaño de la plaza.
    escala_l, escala_a = pl / g["plaza_largo_mm"], pa / g["plaza_ancho_mm"]
    nivel = g["niveles"][-1]
    for n in g["niveles"]:
        if n["largo_max"] is None:
            continue
        if largo_mm <= n["largo_max"] * escala_l and ancho_con_espejos_mm <= n["ancho_max"] * escala_a:
            nivel = n
            break
    lateral = (pa - (ancho_sin_espejos_mm or ancho_con_espejos_mm)) / 2
    return {
        "nivel": nivel["nivel"], "etiqueta": nivel["etiqueta"],
        "holgura_longitudinal_mm": round(pl - largo_mm),
        "espacio_lateral_por_lado_mm": round(lateral),
        "plaza_mm": [pl, pa],
    }


def baul_objetos(litros: float | None) -> list[dict[str, Any]]:
    if not litros:
        return []
    objetos = cfg("indices")["baul_objetos_litros"]
    return [{"objeto": k, "cantidad": math.floor(litros / v), "litros_por_objeto": v} for k, v in objetos.items()]


def comodidad_trasera(eje_mm: float | None, ancho_mm: float | None) -> dict[str, Any] | None:
    if not eje_mm or not ancho_mm:
        return None
    c = cfg("indices")["comodidad_trasera"]
    if eje_mm >= c["eje_bueno_mm"] and ancho_mm >= c["ancho_bueno_mm"]:
        etiqueta = "Amplia para tres adultos"
    elif eje_mm >= c["eje_justo_mm"]:
        etiqueta = "Cómoda para dos adultos"
    else:
        etiqueta = "Justa para adultos"
    return {"etiqueta": etiqueta, "estado": "estimado"}
