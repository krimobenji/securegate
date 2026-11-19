"""Tests du détecteur de secrets."""
from pathlib import Path

from security.secret_scan import main, scanner_fichier


def ecrire(dossier, nom, contenu):
    fichier = dossier / nom
    fichier.write_text(contenu, encoding="utf-8")
    return fichier


def test_fichier_propre_sans_alerte(tmp_path):
    fichier = ecrire(tmp_path, "propre.py", "valeur = 42\n")
    assert scanner_fichier(fichier) == []


def test_mot_de_passe_en_clair_detecte(tmp_path):
    fichier = ecrire(tmp_path, "mauvais.py", 'password = "azerty123"\n')
    resultats = scanner_fichier(fichier)
    assert len(resultats) == 1
    assert resultats[0][1] == 1
    assert resultats[0][2] == "mot-de-passe-en-clair"


def test_lecture_dans_environnement_acceptee(tmp_path):
    fichier = ecrire(tmp_path, "ok.py", 'password = os.environ.get("MDP")\n')
    assert scanner_fichier(fichier) == []


def test_cle_privee_detectee(tmp_path):
    fichier = ecrire(tmp_path, "cle.txt", "-----BEGIN PRIVATE KEY-----\n")
    assert scanner_fichier(fichier)[0][2] == "cle-privee"


def test_ligne_marquee_nosecret_ignoree(tmp_path):
    fichier = ecrire(tmp_path, "exemple.py", 'password = "azerty123"  # nosecret\n')
    assert scanner_fichier(fichier) == []


def test_code_retour_selon_les_resultats(tmp_path):
    propre = tmp_path / "propre"
    propre.mkdir()
    ecrire(propre, "a.py", "x = 1\n")
    sale = tmp_path / "sale"
    sale.mkdir()
    ecrire(sale, "b.py", 'password = "azerty123"\n')
    assert main(["scan", str(propre)]) == 0
    assert main(["scan", str(sale)]) == 1
