"""Buscador de reseñas honestas y reseña completa."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Query

from ..db import fiabilidad_por_id, fuentes_por_id, todos_los_vehiculos
from .vehiculos import _recalls, _resolver, buscar_ids_texto, tarjeta
from ..db import vehiculos_por_id
from ..services.puntaje import etiqueta_fiabilidad
from ..services.config import cfg

router = APIRouter(prefix="/api/fiabilidad", tags=["Fiabilidad"])

PREGUNTAS_POR_COMPONENTE = {
    "caja": ("Pide el historial de cambios de aceite de la caja y pregunta si se ha reparado.",
             "En la prueba, arranca y frena varias veces en subida: busca trepidación, tirones o patinamiento."),
    "motor": ("Pregunta por el tipo de aceite usado y los intervalos reales de cambio.",
              "En frío, revisa humo al encender y ruidos metálicos; en caliente, pérdida de potencia en subida."),
    "correa": ("Exige la factura del último cambio de correa de distribución.",
               "Revisa con un técnico el estado del aceite y la presión: la luz de aceite no debe encender."),
    "turbo": ("Pregunta si el turbo o su actuador han sido reparados.",
              "Acelera a fondo en tercera: el empuje debe ser progresivo, sin silbidos ni pérdidas."),
    "batería": ("Pide el reporte de salud de la batería (SOH) en el concesionario.",
                "Verifica la autonomía mostrada al 100% contra la homologada."),
}


def _checklist(fallas: list[dict]) -> list[dict]:
    items = []
    for fa in fallas:
        comp = fa["componente"].lower()
        clave = next((k for k in PREGUNTAS_POR_COMPONENTE if k in comp or (k == "caja" and ("cvt" in comp or "embrague" in comp or "mecatr" in comp))), None)
        pregunta, prueba = PREGUNTAS_POR_COMPONENTE.get(clave, (
            f"Pregunta al vendedor si ha tenido problemas con: {fa['componente'].lower()}.",
            "Haz que un técnico independiente lo revise antes de pagar."))
        items.append({"componente": fa["componente"], "severidad": fa["severidad"], "que_revisar": fa["descripcion"],
                      "que_preguntar": pregunta, "prueba_de_manejo": prueba, "km_tipico": fa["km_tipico"]})
    return items


@router.get("", summary="Buscador de reseñas")
def buscar(q: str | None = Query(None, max_length=80), marca: list[str] = Query([]),
           puntaje_min: float = Query(1, ge=1, le=10), puntaje_max: float = Query(10, ge=1, le=10),
           mantenimiento: list[str] = Query([]), depreciacion: list[str] = Query([]),
           solo_alertas_rojas: bool = False, limite: int = Query(60, ge=1, le=400)) -> dict[str, Any]:
    vs = list(todos_los_vehiculos())
    if q:
        ids = buscar_ids_texto(q)
        if ids is not None:
            orden = {i: n for n, i in enumerate(ids)}
            vs = sorted([v for v in vs if v["id"] in orden], key=lambda v: orden[v["id"]])
    fs = fiabilidad_por_id()
    out = []
    for v in vs:
        f = fs[v["id"]]
        if marca and v["marca"].lower() not in {m.lower() for m in marca}:
            continue
        if not puntaje_min <= f["puntaje_fiabilidad"] <= puntaje_max:
            continue
        if mantenimiento and f["nivel_costo_mantenimiento"] not in mantenimiento:
            continue
        if depreciacion and f["depreciacion_estimada"] not in depreciacion:
            continue
        if solo_alertas_rojas and not v["tiene_alerta_roja"]:
            continue
        out.append({**tarjeta(v), "etiqueta_fiabilidad": etiqueta_fiabilidad(f["puntaje_fiabilidad"]),
                    "linea_veredicto": f["veredicto_honesto"].split(". ")[0][:180],
                    "nivel_costo_mantenimiento": f["nivel_costo_mantenimiento"],
                    "depreciacion_estimada": f["depreciacion_estimada"],
                    "alertas": f["alertas"]})
    if not q:
        out.sort(key=lambda x: (not x["tiene_alerta_roja"], x["puntaje_fiabilidad"]))
    return {"total": len(out), "resultados": out[:limite]}


@router.get("/{id_o_slug}", summary="Reseña completa con fallas, recalls y checklist")
def resena(id_o_slug: str) -> dict[str, Any]:
    v = _resolver(id_o_slug)
    f = fiabilidad_por_id()[v["id"]]
    fuentes = fuentes_por_id()
    fallas = [{**fa, "fuentes": [fuentes.get(x) for x in fa["fuentes_ids"]]} for fa in f["fallas_comunes_y_contras"]]
    return {
        "vehiculo": tarjeta(v),
        "puntaje_fiabilidad": f["puntaje_fiabilidad"], "etiqueta": etiqueta_fiabilidad(f["puntaje_fiabilidad"]),
        "desglose": f["desglose"], "pesos": cfg("fiabilidad")["pesos"],
        "costos": {k: f[k] for k in ("nivel_costo_mantenimiento", "costo_mantenimiento_anual_cop", "costo_primeros_60000km_cop",
                                     "disponibilidad_repuestos", "depreciacion_estimada", "retencion_valor")},
        "veredicto_honesto": f["veredicto_honesto"], "para_quien_si": f["para_quien_si"], "para_quien_no": f["para_quien_no"],
        "pros_reales": f["pros_reales"], "fallas_comunes_y_contras": fallas, "alertas": f["alertas"],
        "recalls": _recalls(v), "checklist_usado": _checklist(f["fallas_comunes_y_contras"]),
        "alternativas": [tarjeta(vehiculos_por_id()[i]) for i in f["alternativas_recomendadas"] if i in vehiculos_por_id()],
        "fuentes": [fuentes.get(x) for x in f["fuentes_ids"]],
        "ultima_verificacion": v["ultima_verificacion"],
        "aviso_legal": "Opinión editorial basada en fuentes públicas citadas; no es un diagnóstico mecánico de un vehículo en particular.",
    }
