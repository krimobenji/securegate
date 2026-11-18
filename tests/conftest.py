"""Fixtures partagées par les tests."""
import pytest

from app.main import create_app


@pytest.fixture
def db_path(tmp_path):
    return str(tmp_path / "test.db")


@pytest.fixture
def client(db_path):
    return create_app(db_path=db_path).test_client()
