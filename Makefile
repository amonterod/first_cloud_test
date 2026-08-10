# Makefile para tareas comunes

.PHONY: help install test lint format clean run

help:
	@echo "Comandos disponibles:"
	@echo "  install    - Instalar dependencias"
	@echo "  test       - Ejecutar tests"
	@echo "  lint       - Ejecutar linters"
	@echo "  format     - Formatear codigo"
	@echo "  clean      - Limpiar archivos temporales"
	@echo "  run        - Ejecutar aplicacion"

install:
	pip install -r requirements-dev.txt

test:
	pytest tests/ -v --cov=src --cov-report=html

lint:
	flake8 src/ tests/
	mypy src/

format:
	black src/ tests/
	isort src/ tests/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .mypy_cache htmlcov .coverage

run:
	python src/main.py
