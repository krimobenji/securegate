#!/usr/bin/env bash
# Lance les règles Semgrep de SecureGate.
# Code de retour : 0 si aucune alerte, 1 si une règle est enfreinte.
CIBLES=("$@")
if [ ${#CIBLES[@]} -eq 0 ]; then
  CIBLES=(app)
fi
exec semgrep \
  --config security/semgrep/rules.yml \
  --metrics=off \
  --disable-version-check \
  --error \
  --quiet \
  "${CIBLES[@]}"
