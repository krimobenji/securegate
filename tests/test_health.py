"""Tests fonctionnels de la route /health."""
from app.main import VERSION


def test_health_retourne_ok(client):
    reponse = client.get("/health")
    assert reponse.status_code == 200
    assert reponse.get_json() == {"status": "ok", "version": VERSION}


def test_route_inconnue_retourne_404(client):
    reponse = client.get("/nimporte-quoi")
    assert reponse.status_code == 404
