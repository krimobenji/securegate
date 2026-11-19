"""Accès à la base SQLite (requêtes paramétrées uniquement)."""
import sqlite3
from contextlib import closing

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user'
)
"""


def get_connection(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path):
    """Crée la table des utilisateurs si elle n'existe pas."""
    with closing(get_connection(db_path)) as conn:
        conn.execute(SCHEMA)
        conn.commit()


def create_user(db_path, username, password_hash):
    """Ajoute un utilisateur. Retourne False si le nom est déjà pris."""
    with closing(get_connection(db_path)) as conn:
        try:
            conn.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            return False
    return True


def get_user(db_path, username):
    """Retourne l'utilisateur (dictionnaire) ou None."""
    with closing(get_connection(db_path)) as conn:
        row = conn.execute(
            "SELECT id, username, password_hash, role FROM users WHERE username = ?",
            (username,),
        ).fetchone()
    return dict(row) if row else None


def search_users(db_path, term):
    """Recherche par nom (contient le texte). Ne renvoie jamais l'empreinte."""
    with closing(get_connection(db_path)) as conn:
        rows = conn.execute(
            "SELECT id, username, role FROM users WHERE username LIKE ? ORDER BY username",
            ("%" + term + "%",),
        ).fetchall()
    return [dict(r) for r in rows]
