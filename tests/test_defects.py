"""Tests du catalogue de défauts (sur une copie temporaire du code)."""
import shutil
from pathlib import Path

import pytest

from scripts import defect

RACINE = Path(__file__).resolve().parent.parent


@pytest.fixture
def projet(tmp_path, monkeypatch):
    """Copie du dossier app/ dans un dossier temporaire, remise à l'état sain."""
    shutil.copytree(RACINE / "app", tmp_path / "app", ignore=shutil.ignore_patterns("__pycache__"))
    monkeypatch.chdir(tmp_path)
    defect.main(["defect.py", "fix-all"])
    return tmp_path


def contenu(dossier):
    return {str(p): p.read_text(encoding="utf-8") for p in sorted((dossier / "app").glob("*.py"))}


def test_tous_les_defauts_sains_sur_le_code_sain(projet):
    for nom in defect.CATALOGUE:
        assert defect.etat(nom) == "sain"


@pytest.mark.parametrize("nom", list(defect.CATALOGUE))
def test_injection_puis_correction_restaure_le_code(projet, nom):
    avant = contenu(projet)
    assert defect.main(["defect.py", "inject", nom]) == 0
    assert defect.etat(nom) == "injecté"
    assert contenu(projet) != avant
    assert defect.main(["defect.py", "fix", nom]) == 0
    assert contenu(projet) == avant


def test_injection_idempotente(projet):
    defect.main(["defect.py", "inject", "sqli"])
    apres_une_fois = contenu(projet)
    assert defect.main(["defect.py", "inject", "sqli"]) == 0
    assert contenu(projet) == apres_une_fois


def test_nom_de_defaut_inconnu_code_64(projet):
    assert defect.main(["defect.py", "inject", "inexistant"]) == 64


def test_action_absente_code_64(projet):
    assert defect.main(["defect.py"]) == 64


def test_fichier_modifie_a_la_main_refuse_code_2(projet):
    (projet / "app" / "repository.py").write_text("x = 1\n", encoding="utf-8")
    assert defect.main(["defect.py", "inject", "sqli"]) == 2


def test_liste_des_defauts_code_0(projet, capsys):
    assert defect.main(["defect.py", "list"]) == 0
    sortie = capsys.readouterr().out
    for nom in defect.CATALOGUE:
        assert nom in sortie


def test_fix_all_remet_tout_sain(projet):
    for nom in defect.CATALOGUE:
        defect.main(["defect.py", "inject", nom])
    assert defect.main(["defect.py", "fix-all"]) == 0
    assert all(defect.etat(nom) == "sain" for nom in defect.CATALOGUE)
