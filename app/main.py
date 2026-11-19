"""Application cible de SecureGate : annuaire d'utilisateurs minimal."""
from flask import Flask, jsonify, request

from app import config, repository
from app.security_utils import hash_password, verify_password

VERSION = "0.2.0"
MIN_PASSWORD_LENGTH = 8


def create_app(db_path=None):
    app = Flask(__name__)
    app.json.ensure_ascii = False
    chemin = db_path or config.DATABASE_PATH
    repository.init_db(chemin)

    @app.get("/health")
    def health():
        return jsonify(status="ok", version=VERSION)

    @app.post("/register")
    def register():
        data = request.get_json(silent=True) or {}
        username = str(data.get("username", "")).strip()
        password = str(data.get("password", ""))
        if not username or len(password) < MIN_PASSWORD_LENGTH:
            return jsonify(error="nom requis et mot de passe d'au moins 8 caractères"), 400
        if not repository.create_user(chemin, username, hash_password(password)):
            return jsonify(error="nom d'utilisateur déjà pris"), 409
        return jsonify(message="utilisateur créé", username=username), 201

    @app.post("/login")
    def login():
        data = request.get_json(silent=True) or {}
        username = str(data.get("username", "")).strip()
        password = str(data.get("password", ""))
        user = repository.get_user(chemin, username)
        if user is None or not verify_password(password, user["password_hash"]):
            return jsonify(error="identifiants invalides"), 401
        return jsonify(message="authentification réussie", username=user["username"])

    @app.get("/users")
    def users():
        nom = request.args.get("name")
        if nom is None:
            return jsonify(error="paramètre 'name' requis"), 400
        return jsonify(repository.search_users(chemin, nom))

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5000)
