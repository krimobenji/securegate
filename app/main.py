"""Application cible de SecureGate : API minimale."""
from flask import Flask, jsonify

VERSION = "0.1.0"


def create_app():
    app = Flask(__name__)

    @app.get("/health")
    def health():
        return jsonify(status="ok", version=VERSION)

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5000)
