"""Errores con formato único {codigo, mensaje, detalle}."""
from __future__ import annotations

from typing import Any

from fastapi import HTTPException


class ErrorApi(HTTPException):
    def __init__(self, status: int, codigo: str, mensaje: str, detalle: Any = None) -> None:
        super().__init__(status_code=status, detail={"codigo": codigo, "mensaje": mensaje, "detalle": detalle})


def no_encontrado(recurso: str, ident: Any) -> ErrorApi:
    return ErrorApi(404, "no_encontrado", f"{recurso} no encontrado", {"id": ident})


def invalido(mensaje: str, detalle: Any = None) -> ErrorApi:
    return ErrorApi(422, "parametro_invalido", mensaje, detalle)
