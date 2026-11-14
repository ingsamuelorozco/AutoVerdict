# Cómo contribuir

1. Los datos viven en `data/`. Edita el YAML de la marca en `data/vehiculos/`, nunca la base de datos directamente.
2. Cada cifra nueva necesita `fuente` y fecha. Si no la puedes confirmar, márcala como estimada en `campos_estimados` y explica la lógica.
3. Ejecuta `python scripts/seed.py` y `python scripts/verify_data.py`; ambos deben terminar sin errores.
4. Ejecuta `pytest -q` y, en `frontend/`, `npm run test` y `npm run build`.
5. Usa commits convencionales (`feat:`, `fix:`, `data:`, `docs:`, `chore:`) y abre un pull request.

Las reseñas son opinión editorial basada en fuentes públicas: no publiques afirmaciones sin una fuente citada.
