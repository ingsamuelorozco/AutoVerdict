"""Estimador orientativo del seguro todo riesgo. Siempre devuelve un rango."""
from __future__ import annotations

from typing import Any

from .config import ELECTRIFICADOS, cfg, ciudad, meta


def todo_riesgo(valor_asegurado_cop: float, segmento: str, ciudad_id: str | None = None,
                edad_conductor: str = "36-55", uso: str = "particular", antiguedad_anios: int = 0,
                riesgo_hurto: str = "Medio", deducible: str = "1", tipo_combustible: str | None = None) -> dict[str, Any]:
    c = cfg("seguros")
    cd = ciudad(ciudad_id)
    tasa = c["tasa_base_por_segmento"].get(segmento, c["tasa_base_defecto"])
    factores = {
        "ciudad": cd["riesgo_factor"],
        "edad_conductor": c["factor_edad_conductor"].get(edad_conductor, 1.0),
        "uso": c["factor_uso"].get(uso, 1.0),
        "antiguedad": 1 + c["factor_antiguedad_por_anio"] * antiguedad_anios,
        "riesgo_hurto": c["factor_riesgo_hurto"].get(riesgo_hurto, 1.0),
        "deducible": c["factor_deducible"].get(str(deducible), 1.0),
        "electrificado": c["factor_electrificado"] if tipo_combustible in ELECTRIFICADOS else 1.0,
    }
    producto = 1.0
    for f in factores.values():
        producto *= f
    fijos = sum(c["componentes_fijos_cop"].values())
    central = valor_asegurado_cop * tasa * producto + fijos
    amp = c["amplitud_rango"]
    return {
        "valor_asegurado_cop": round(valor_asegurado_cop), "tasa_base": tasa, "factores": factores,
        "componentes_fijos_cop": c["componentes_fijos_cop"],
        "prima_anual_min_cop": round(central * (1 - amp), -3),
        "prima_anual_central_cop": round(central, -3),
        "prima_anual_max_cop": round(central * (1 + amp), -3),
        "aviso": c["aviso"], **meta("seguros"),
    }
