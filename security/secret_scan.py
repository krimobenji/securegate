#!/usr/bin/env python3
"""Détecteur local de secrets écrits en dur dans le code."""
import re
import sys
from pathlib import Path

REGLES = [
    (
        "mot-de-passe-en-clair",
        re.compile(r"""(password|passwd|pwd|mot_de_passe)\s*=\s*["'][^"']{4,}["']""", re.IGNORECASE),
        "Lire la valeur dans une variable d'environnement (os.environ).",
    ),
    (
        "cle-ou-jeton-en-clair",
        re.compile(r"""(api[_-]?key|secret|token)\s*=\s*["'][^"']{8,}["']""", re.IGNORECASE),
        "Ne pas écrire de clé dans le code : utiliser une variable d'environnement.",
    ),
    (
        "cle-privee",
        re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        "Retirer la clé privée du dépôt et la révoquer.",
    ),
]

EXTENSIONS = {".py", ".env", ".cfg", ".ini", ".yml", ".yaml", ".json", ".txt", ".toml"}
EXCLUS = {".venv", ".git", "__pycache__"}


def scanner_fichier(chemin):
    """Retourne la liste des (fichier, ligne, règle, conseil) trouvés dans un fichier."""
    trouvailles = []
    try:
        lignes = chemin.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return trouvailles
    for numero, ligne in enumerate(lignes, start=1):
        if "nosecret" in ligne:
            continue
        for nom, motif, conseil in REGLES:
            if motif.search(ligne):
                trouvailles.append((chemin, numero, nom, conseil))
    return trouvailles


def lister_fichiers(cible):
    if cible.is_file():
        return [cible]
    return sorted(
        p for p in cible.rglob("*")
        if p.is_file() and p.suffix in EXTENSIONS and not EXCLUS.intersection(p.parts)
    )


def main(argv):
    cibles = [Path(a) for a in argv[1:]] or [Path("app")]
    trouvailles = []
    for cible in cibles:
        for fichier in lister_fichiers(cible):
            trouvailles += scanner_fichier(fichier)
    if not trouvailles:
        print("Aucun secret détecté.")
        return 0
    for chemin, numero, nom, conseil in trouvailles:
        print("%s:%d  règle : %s  |  conseil : %s" % (chemin, numero, nom, conseil))
    print("%d secret(s) potentiel(s) détecté(s)." % len(trouvailles))
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
