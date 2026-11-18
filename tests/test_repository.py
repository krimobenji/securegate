"""Tests de l'accès à la base SQLite."""
import pytest

from app.repository import create_user, get_user, init_db, search_users


@pytest.fixture
def db(tmp_path):
    chemin = str(tmp_path / "test.db")
    init_db(chemin)
    return chemin


def test_creation_et_lecture_utilisateur(db):
    assert create_user(db, "salma", "hash1") is True
    utilisateur = get_user(db, "salma")
    assert utilisateur["username"] == "salma"
    assert utilisateur["role"] == "user"


def test_nom_deja_pris_refuse(db):
    create_user(db, "salma", "hash1")
    assert create_user(db, "salma", "hash2") is False


def test_utilisateur_inconnu_retourne_none(db):
    assert get_user(db, "personne") is None


def test_recherche_partielle(db):
    create_user(db, "salma", "h")
    create_user(db, "salim", "h")
    create_user(db, "youssef", "h")
    noms = [u["username"] for u in search_users(db, "sal")]
    assert noms == ["salim", "salma"]


def test_recherche_sans_resultat(db):
    create_user(db, "salma", "h")
    assert search_users(db, "zzz") == []


def test_recherche_ne_renvoie_pas_l_empreinte(db):
    create_user(db, "salma", "hash-secret")
    resultat = search_users(db, "salma")
    assert "password_hash" not in resultat[0]


def test_texte_hostile_traite_comme_simple_texte(db):
    create_user(db, "salma", "h")
    assert search_users(db, "x' OR '1'='1") == []
