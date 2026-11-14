"""Curva de valor residual y depreciación."""
from __future__ import annotations

from typing import Any

from .config import cfg, meta

HITOS = (1, 3, 5, 7, 10)


def curva_base(etiqueta: str | None) -> dict[str, float]:
    curvas = cfg("depreciacion")["curvas"]
    return {k: float(v) for k, v in curvas.get(etiqueta or "Media", curvas["Media"]).items()}


def retencion_completa(retencion: dict[str, float] | None, etiqueta: str | None) -> dict[str, float]:
    """Completa la curva a 1, 3, 5, 7 y 10 años; el año 10 se extrapola si falta."""
    base = curva_base(etiqueta)
    r = {str(k): float(v) for k, v in (retencion or {}).items()}
    out = {}
    for h in HITOS:
        out[str(h)] = r.get(str(h), base[str(h)])
    if "10" not in r and "7" in r:
        d = cfg("depreciacion")["decaimiento_anual_extrapolacion"]
        out["10"] = round(r["7"] * (1 - d) ** 3, 3)
    return out


def interpolar(curva: dict[str, float], anio: float) -> float:
    if anio <= 0:
        return 1.0
    puntos = [(0, 1.0)] + sorted((int(k), v) for k, v in curva.items())
    for (a0, v0), (a1, v1) in zip(puntos, puntos[1:]):
        if a0 <= anio <= a1:
            return v0 + (v1 - v0) * (anio - a0) / (a1 - a0)
    d = cfg("depreciacion")["decaimiento_anual_extrapolacion"]
    ultimo_a, ultimo_v = puntos[-1]
    return ultimo_v * (1 - d) ** (anio - ultimo_a)


def curva_reventa(precio_cop: float, retencion: dict[str, float] | None, etiqueta: str | None,
                  trm: float | None = None) -> dict[str, Any]:
    curva = retencion_completa(retencion, etiqueta)
    puntos = []
    for h in HITOS:
        v = precio_cop * curva[str(h)]
        puntos.append({"anio": h, "retencion": curva[str(h)], "valor_cop": round(v, -3),
                       "valor_usd": round(v / trm) if trm else None})
    perdida_5 = precio_cop * (1 - curva["5"]) / 5
    return {"puntos": puntos, "perdida_anual_aprox_cop": round(perdida_5, -3), "etiqueta": etiqueta,
            "estado": "estimado", **meta("depreciacion")}
