#!/usr/bin/env bash
# Analyse Bandit : gravité MEDIUM et plus.
# Code de retour : 0 si aucune alerte, 1 sinon.
exec bandit -r "${@:-app}" -ll -q

