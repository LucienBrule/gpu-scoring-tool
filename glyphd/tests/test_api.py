import pytest
from glyphd.api.router import create_app

def test_app_creation(app):
    """Test that the FastAPI app can be created successfully."""
    assert app is not None

def test_health_endpoint(client):
    """Test that the health endpoint returns the expected response."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
