"""Tests fonctionnels des routes /register, /login et /users."""
from app.repository import get_user


def inscrire(client, nom="salma", mdp="MotDePasse123"):
    return client.post("/register", json={"username": nom, "password": mdp})


def test_inscription_reussie(client):
    reponse = inscrire(client)
    assert reponse.status_code == 201
    assert reponse.get_json()["username"] == "salma"


def test_inscription_mot_de_passe_trop_court(client):
    reponse = inscrire(client, mdp="court")
    assert reponse.status_code == 400


def test_inscription_sans_donnees(client):
    reponse = client.post("/register")
    assert reponse.status_code == 400


def test_inscription_nom_deja_pris(client):
    inscrire(client)
    reponse = inscrire(client)
    assert reponse.status_code == 409


def test_mot_de_passe_stocke_hache(client, db_path):
    inscrire(client)
    stocke = get_user(db_path, "salma")["password_hash"]
    assert "MotDePasse123" not in stocke
    assert stocke.startswith("200000$")


def test_connexion_reussie(client):
    inscrire(client)
    reponse = client.post("/login", json={"username": "salma", "password": "MotDePasse123"})
    assert reponse.status_code == 200


def test_connexion_mauvais_mot_de_passe(client):
    inscrire(client)
    reponse = client.post("/login", json={"username": "salma", "password": "faux-mot-de-passe"})
    assert reponse.status_code == 401


def test_connexion_utilisateur_inconnu(client):
    reponse = client.post("/login", json={"username": "personne", "password": "MotDePasse123"})
    assert reponse.status_code == 401


def test_recherche_utilisateurs(client):
    inscrire(client, "salma")
    inscrire(client, "youssef")
    reponse = client.get("/users?name=sal")
    assert reponse.status_code == 200
    donnees = reponse.get_json()
    assert [u["username"] for u in donnees] == ["salma"]
    assert "password_hash" not in donnees[0]


def test_recherche_sans_parametre(client):
    reponse = client.get("/users")
    assert reponse.status_code == 400
