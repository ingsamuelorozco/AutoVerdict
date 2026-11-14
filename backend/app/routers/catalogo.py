"""Catálogo en cascada: marca → modelo → año → versión."""
from __future__ import annotations

from collections import Counter
from functools import lru_cache

from fastapi import APIRouter, Query

from ..db import todos_los_vehiculos

router = APIRouter(prefix="/api/catalogo", tags=["Catálogo"])


@lru_cache(maxsize=1)
def _marcas() -> list[dict]:
    c = Counter(v["marca"] for v in todos_los_vehiculos())
    return [{"marca": m, "versiones": n} for m, n in sorted(c.items())]


@lru_cache(maxsize=256)
def _modelos(marca: str) -> list[dict]:
    c = Counter(v["modelo"] for v in todos_los_vehiculos() if v["marca"].lower() == marca.lower())
    return [{"modelo": m, "versiones": n} for m, n in sorted(c.items())]


@router.get("/marcas", summary="Marcas con conteo de versiones")
def marcas() -> list[dict]:
    return _marcas()


@router.get("/modelos", summary="Modelos de una marca")
def modelos(marca: str = Query(..., examples=["Mazda"])) -> list[dict]:
    return _modelos(marca)


@router.get("/anios", summary="Años disponibles de un modelo")
def anios(marca: str = Query(..., examples=["Mazda"]), modelo: str = Query(..., examples=["CX-30"])) -> list[int]:
    return sorted({v["anio"] for v in todos_los_vehiculos()
                   if v["marca"].lower() == marca.lower() and v["modelo"].lower() == modelo.lower()}, reverse=True)


@router.get("/versiones", summary="Versiones con id, precio y etiqueta")
def versiones(marca: str = Query(..., examples=["Mazda"]), modelo: str = Query(..., examples=["CX-30"]),
              anio: int = Query(..., examples=[2026])) -> list[dict]:
    return [{"id": v["id"], "slug": v["slug"], "version": v["version"], "precio_base_cop": v["precio_base_cop"],
             "etiqueta": f"{v['version']} · {v['tipo_combustible']}", "tiene_alerta_roja": v["tiene_alerta_roja"]}
            for v in todos_los_vehiculos()
            if v["marca"].lower() == marca.lower() and v["modelo"].lower() == modelo.lower() and v["anio"] == anio]
