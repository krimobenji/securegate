"""Hachage et vérification des mots de passe (PBKDF2-SHA256)."""
import hashlib
import hmac
import os

ITERATIONS = 200_000


def hash_password(password):
    """Retourne 'iterations$sel$empreinte' (sel et empreinte en hexadécimal)."""
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ITERATIONS)
    return "%d$%s$%s" % (ITERATIONS, salt.hex(), digest.hex())


def verify_password(password, stored):
    """Vérifie un mot de passe contre l'empreinte stockée."""
    try:
        iterations, salt_hex, digest_hex = stored.split("$")
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(digest_hex)
        iterations = int(iterations)
    except ValueError:
        return False
    candidate = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return hmac.compare_digest(candidate, expected)
