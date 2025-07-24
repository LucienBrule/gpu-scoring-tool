import pytest
from fastapi.testclient import TestClient
from click.testing import CliRunner

from glyphd.api.router import create_app
from glyphd.cli import cli

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