PYTHON ?= python3
VENV   := .venv
PY     := $(VENV)/bin/python
export PATH := $(CURDIR)/$(VENV)/bin:$(PATH)

.DEFAULT_GOAL := help
.PHONY: help setup test coverage secrets bandit semgrep securite

help: ## Affiche cette aide
	@grep -E '^[a-z-]+:.*##' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  make %-8s %s\n", $$1, $$2}'

setup: ## Crée l'environnement virtuel et installe les dépendances
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/pip install -r requirements-dev.txt

test: ## Lance les tests fonctionnels (pytest)
	$(PY) -m pytest -v

coverage: ## Tests avec couverture de code (seuil bloquant : 80 %)
	$(PY) -m pytest -q --cov=app --cov-report=term-missing --cov-fail-under=80

secrets: ## Détecteur de secrets (bloquant)
	$(PY) security/secret_scan.py app

bandit: ## Analyse Bandit, gravité MEDIUM et plus (bloquant)
	./scripts/run_bandit.sh

semgrep: ## Règles Semgrep maison (bloquant)
	./scripts/run_semgrep.sh

securite: secrets bandit semgrep ## Les trois contrôles de sécurité à la suite
