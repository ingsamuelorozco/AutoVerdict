"""Vehículos actualizados: qué cambió y si vale la pena."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Query

from ..db import consultar, fuentes_por_id, uno, vehiculos_por_id
from ..errores import no_encontrado
from .vehiculos import tarjeta

router = APIRouter(prefix="/api/actualizados", tags=["Actualizados"])


def _enriquecer(a: dict) -> dict:
    vs = vehiculos_por_id()
    a["vehiculos"] = [tarjeta(vs[i]) for i in a["vehiculo_ids"] if i in vs]
    a["anterior"] = tarjeta(vs[a["vehiculo_anterior_id"]]) if a.get("vehiculo_anterior_id") in vs else None
    return a


@router.get("", summary="Lista de actualizaciones con filtros")
def listar(tipo: list[str] = Query([]), categoria: list[str] = Query([]), marca: list[str] = Query([]),
           anio: int | None = None, segmento: list[str] = Query([])) -> dict[str, Any]:
    out = []
    for a in consultar("SELECT * FROM actualizaciones ORDER BY fecha_lanzamiento_colombia DESC"):
        if tipo and a["tipo"] not in tipo:
            continue
        if categoria and not set(categoria) & set(a["categorias"]):
            continue
        if marca and a["marca"] not in marca:
            continue
        if anio and a["anio_modelo"] != anio:
            continue
        if segmento and a["segmento"] not in segmento:
            continue
        out.append(_enriquecer(a))
    return {"total": len(out), "resultados": out}


@router.get("/{aid}", summary="Detalle de una actualización con antes y ahora")
def detalle(aid: int) -> dict[str, Any]:
    a = uno("SELECT * FROM actualizaciones WHERE id = ?", (aid,))
    if not a:
        raise no_encontrado("Actualización", aid)
    a = _enriquecer(a)
    a["fuentes"] = [fuentes_por_id().get(f) for f in a["fuentes_ids"]]
    return a
