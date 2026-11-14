PY ?= python
.PHONY: instalar sembrar verificar api web pruebas build docker
instalar:
	$(PY) -m pip install -r backend/requirements.txt -r backend/requirements-dev.txt
	cd frontend && npm install
sembrar:
	$(PY) scripts/seed.py
verificar:
	$(PY) scripts/verify_data.py && $(PY) scripts/verify_images.py
api:
	$(PY) -m uvicorn backend.app.main:app --reload --port 8000
web:
	cd frontend && npm run dev
pruebas:
	$(PY) -m pytest -q && cd frontend && npm run test && npm run test:e2e
build:
	cd frontend && npm run build
docker:
	docker compose up --build
