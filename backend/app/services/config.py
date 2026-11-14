"""Carga de archivos de configuración JSON (tarifas, tasas, umbrales).

Todos los parámetros financieros y umbrales viven en backend/app/config/*.json.
El código nunca debe incrustar esas cifras.
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"


@lru_cache(maxsize=32)
def cfg(nombre: str) -> dict[str, Any]:
    ruta = CONFIG_DIR / f"{nombre}.json"
    with ruta.open(encoding="utf-8") as f:
        return json.load(f)


def ciudad(ciudad_id: str | None) -> dict[str, Any]:
    datos = cfg("ciudades")
    cid = ciudad_id or datos["ciudad_defecto"]
    if cid not in datos["ciudades"]:
        raise KeyError(cid)
    return {"id": cid, **datos["ciudades"][cid]}


def ciudades_ids() -> list[str]:
    return list(cfg("ciudades")["ciudades"].keys())


def meta(nombre: str) -> dict[str, Any]:
    """Metadatos de vigencia para mostrar junto a cada resultado."""
    c = cfg(nombre)
    return {k: c.get(k) for k in ("vigencia", "fuente_url", "fecha_consulta", "estado") if k in c}


ELECTRIFICADOS = {"Híbrido Completo HEV", "Híbrido Ligero MHEV", "Híbrido Enchufable PHEV", "100% Eléctrico BEV"}
BEV = "100% Eléctrico BEV"
PHEV = "Híbrido Enchufable PHEV"
HEV = "Híbrido Completo HEV"
MHEV = "Híbrido Ligero MHEV"
