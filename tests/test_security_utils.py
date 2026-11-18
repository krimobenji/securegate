"""Tests du hachage des mots de passe."""
from app.security_utils import hash_password, verify_password


def test_hash_ne_contient_pas_le_mot_de_passe():
    h = hash_password("MotDePasse123")
    assert "MotDePasse123" not in h


def test_deux_hash_du_meme_mot_de_passe_different():
    assert hash_password("MotDePasse123") != hash_password("MotDePasse123")


def test_verification_bon_mot_de_passe():
    h = hash_password("MotDePasse123")
    assert verify_password("MotDePasse123", h) is True


def test_verification_mauvais_mot_de_passe():
    h = hash_password("MotDePasse123")
    assert verify_password("autre-chose", h) is False


def test_empreinte_mal_formee_refusee():
    assert verify_password("MotDePasse123", "n'importe quoi") is False
