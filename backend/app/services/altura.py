"""Índice de altura: potencia efectiva estimada según msnm."""
from __future__ import annotations

from typing import Any

from .config import BEV, cfg, ciudad


def potencia_efectiva(potencia_hp: float | None, alimentacion: str | None, tipo_combustible: str,
                      altitud_msnm: float) -> dict[str, Any] | None:
    if not potencia_hp:
        return None
    c = cfg("altura")
    if tipo_combustible == BEV:
        perdida = 0.0
    else:
        tasa = c["perdida_por_1000m"].get(alimentacion or "Atmosférico", c["perdida_por_1000m"]["Atmosférico"])
        frac = c["fraccion_termica_hibrido"].get(tipo_combustible, 1.0)
        perdida = tasa * altitud_msnm / 1000 * frac
    return {"potencia_hp": potencia_hp, "potencia_efectiva_hp": round(potencia_hp * (1 - perdida)),
            "perdida_pct": round(perdida, 3), "altitud_msnm": altitud_msnm, "estado": "estimado"}


def tabla_ciudades(potencia_hp: float | None, alimentacion: str | None, tipo_combustible: str,
                   ciudad_elegida: str | None = None) -> list[dict[str, Any]]:
    ids = list(cfg("altura")["ciudades_referencia"])
    if ciudad_elegida and ciudad_elegida not in ids:
        ids.append(ciudad_elegida)
    out = []
    for cid in ids:
        cd = ciudad(cid)
        r = potencia_efectiva(potencia_hp, alimentacion, tipo_combustible, cd["altitud_msnm"])
        if r:
            out.append({"ciudad_id": cid, "ciudad": cd["nombre"], **r})
    return out
