"""Configuration lue depuis l'environnement (aucun secret dans le code)."""
import os

DATABASE_PATH = os.environ.get("SECUREGATE_DB", "securegate.db")
