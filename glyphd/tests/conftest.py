import pytest
from click.testing import CliRunner
from fastapi.testclient import TestClient

from glyphd.api.router import create_app


@pytest.fixture
def app():
    """Create a FastAPI app for testing."""
    return create_app()


@pytest.fixture
def client(app):
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def runner():
    """Create a CLI runner for testing."""
    return CliRunner()
