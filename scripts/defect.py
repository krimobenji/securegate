#!/usr/bin/env python3
"""Catalogue de défauts fictifs : injecter ou corriger (réversible, idempotent)."""
import sys
from pathlib import Path

CATALOGUE = {
    "sqli": {
        "description": "Requête SQL construite par concaténation (injection SQL)",
        "detecte_par": "Bandit / Semgrep (code 30)",
        "modifs": [(
            "app/repository.py",
            '''        row = conn.execute(
            "SELECT id, username, password_hash, role FROM users WHERE username = ?",
            (username,),
        ).fetchone()
''',
            '''        row = conn.execute(
            "SELECT id, username, password_hash, role FROM users WHERE username = '" + username + "'"
        ).fetchone()
''',
        )],
    },
    "secret": {
        "description": "Mot de passe fictif écrit en clair dans la configuration",
        "detecte_par": "Détecteur de secrets (code 20)",
        "modifs": [(
            "app/config.py",
            'DATABASE_PATH = os.environ.get("SECUREGATE_DB", "securegate.db")\n',
            'DATABASE_PATH = os.environ.get("SECUREGATE_DB", "securegate.db")\n'
            'ADMIN_PASSWORD = "admin-demo-1234"\n',
        )],
    },
    "weakhash": {
        "description": "Hachage faible MD5 à la place de PBKDF2",
        "detecte_par": "Bandit (code 30)",
        "modifs": [
            (
                "app/security_utils.py",
                '    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ITERATIONS)\n',
                '    digest = hashlib.md5(salt + password.encode("utf-8")).digest()\n',
            ),
            (
                "app/security_utils.py",
                '    candidate = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)\n',
                '    candidate = hashlib.md5(salt + password.encode("utf-8")).digest()\n',
            ),
        ],
    },
    "bug": {
        "description": "Erreur fonctionnelle : un nom déjà pris renvoie 200 au lieu de 409",
        "detecte_par": "pytest (code 10)",
        "modifs": [(
            "app/main.py",
            '''jsonify(error="nom d'utilisateur déjà pris"), 409''',
            '''jsonify(error="nom d'utilisateur déjà pris"), 200''',
        )],
    },
}


def lire(fichier):
    return Path(fichier).read_text(encoding="utf-8")


def est_injecte(modif):
    return modif[2] in lire(modif[0])


def est_sain(modif):
    return modif[1] in lire(modif[0]) and not est_injecte(modif)


def etat(nom):
    modifs = CATALOGUE[nom]["modifs"]
    if all(est_injecte(m) for m in modifs):
        return "injecté"
    if all(est_sain(m) for m in modifs):
        return "sain"
    return "inconnu"


def appliquer(nom, vers_defaut):
    modifs = CATALOGUE[nom]["modifs"]
    courant = etat(nom)
    cible = "injecté" if vers_defaut else "sain"
    if courant == cible:
        print("Défaut « %s » : déjà %s, rien à faire." % (nom, cible))
        return 0
    if courant == "inconnu":
        print("Défaut « %s » : le code ne correspond ni à la version saine ni à la version "
              "avec défaut (fichier modifié à la main ?)." % nom)
        return 2
    for fichier, sain, defaut in modifs:
        ancien, nouveau = (sain, defaut) if vers_defaut else (defaut, sain)
        Path(fichier).write_text(lire(fichier).replace(ancien, nouveau, 1), encoding="utf-8")
    print("Défaut « %s » : %s." % (nom, "injecté" if vers_defaut else "corrigé"))
    return 0


def main(argv):
    if len(argv) < 2 or argv[1] not in ("list", "inject", "fix", "fix-all"):
        print("Usage : defect.py list | inject NOM | fix NOM | fix-all")
        return 64
    action = argv[1]
    if action == "list":
        for nom, info in CATALOGUE.items():
            print("%-9s %-9s %s [%s]" % (nom, etat(nom), info["description"], info["detecte_par"]))
        return 0
    if action == "fix-all":
        code = 0
        for nom in CATALOGUE:
            code = max(code, appliquer(nom, False))
        return code
    if len(argv) < 3 or argv[2] not in CATALOGUE:
        print("Nom de défaut inconnu. Disponibles : %s" % ", ".join(CATALOGUE))
        return 64
    return appliquer(argv[2], action == "inject")


if __name__ == "__main__":
    sys.exit(main(sys.argv))
