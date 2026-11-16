PYTHON ?= python3
VENV   := .venv
PY     := $(VENV)/bin/python

.DEFAULT_GOAL := help
.PHONY: help setup test

help: ## Affiche cette aide
	@grep -E '^[a-z-]+:.*##' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  make %-8s %s\n", $$1, $$2}'

setup: ## Crée l'environnement virtuel et installe les dépendances
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/pip install -r requirements.txt

test: ## Lance les tests fonctionnels (pytest)
	$(PY) -m pytest -v
