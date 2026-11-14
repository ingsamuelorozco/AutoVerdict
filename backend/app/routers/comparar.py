"""Comparador de 2 a 10 vehículos."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from ..db import vehiculo_completo
from ..errores import invalido, no_encontrado
from ..schemas import CompararIn
from ..services.comparador import comparar as comparar_srv
from ..services.config import cfg
from ..services.trm import obtener_trm

router = APIRouter(prefix="/api/comparar", tags=["Comparador"])


@router.post("", summary="Compara 2 a 10 vehículos: filas, ganadores, marcador y puntaje")
def comparar(datos: CompararIn) -> dict[str, Any]:
    if len(set(datos.ids)) != len(datos.ids):
        raise invalido("Hay ids repetidos", {"ids": datos.ids})
    if datos.ciudad and datos.ciudad not in cfg("ciudades")["ciudades"]:
        raise invalido("Ciudad no válida", {"ciudad": datos.ciudad})
    vs = []
    for i in datos.ids:
        v = vehiculo_completo(i)
        if not v:
            raise no_encontrado("Vehículo", i)
        vs.append(v)
    trm = datos.trm or obtener_trm()["valor"]
    res = comparar_srv(vs, datos.ciudad, datos.perfil, datos.referencia_id, trm)
    res.update({"moneda": datos.moneda, "trm": trm})
    return res
