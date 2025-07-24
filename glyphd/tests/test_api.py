import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from glyphd.api.router import create_app
from glyphd.api.models import GPUListingDTO, GPUModelDTO, ReportDTO
from glyphd.core.dependencies import get_insight_report

def test_app_creation(app):
    """Test that the FastAPI app can be created successfully."""
    assert app is not None

def test_health_endpoint(client):
    """Test that the health endpoint returns the expected response."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_listings_endpoint(client):
    """Test that the listings endpoint returns the expected response."""
    response = client.get("/api/listings")
    assert response.status_code == 200
    listings = response.json()
    assert isinstance(listings, list)
    if listings:  # If there are any listings
        # Validate the first listing against the DTO schema
        listing = listings[0]
        assert "canonical_model" in listing
        assert "vram_gb" in listing
        assert "mig_support" in listing
        assert "nvlink" in listing
        assert "tdp_watts" in listing
        assert "price" in listing
        assert "score" in listing

def test_listings_endpoint_with_filters(client):
    """Test that the listings endpoint with filters returns the expected response."""
    # Test filtering by model
    response = client.get("/api/listings?model=H100_PCIE_80GB")
    assert response.status_code == 200
    listings = response.json()
    assert isinstance(listings, list)
    if listings:  # If there are any listings
        for listing in listings:
            assert listing["canonical_model"] == "H100_PCIE_80GB"

    # Test filtering by quantized capability
    response = client.get("/api/listings?quantized=true")
    assert response.status_code == 200
    listings = response.json()
    assert isinstance(listings, list)
    # Note: We can't assert anything about the content here without knowing the data

def test_models_endpoint(client):
    """Test that the models endpoint returns the expected response."""
    response = client.get("/api/models")
    assert response.status_code == 200
    models = response.json()
    assert isinstance(models, list)
    if models:  # If there are any models
        # Validate the first model against the DTO schema
        model = models[0]
        assert "model" in model
        assert "listing_count" in model
        assert "min_price" in model
        assert "median_price" in model
        assert "max_price" in model
        assert "avg_price" in model

def test_report_endpoint(app, client):
    """Test that the report endpoint returns the expected response."""
    # Create a mock report
    mock_report = ReportDTO(
        markdown="# Test Report",
        summary_stats={"test_stat": "test_value"},
        top_ranked=["Test Model 1", "Test Model 2"],
        scoring_weights={
            "vram_weight": 0.3,
            "mig_weight": 0.2,
            "nvlink_weight": 0.1,
            "tdp_weight": 0.2,
            "price_weight": 0.2
        }
    )

    # Override the get_insight_report dependency
    app.dependency_overrides[get_insight_report] = lambda: mock_report

    # Make the request
    response = client.get("/api/report")

    # Clean up the override
    app.dependency_overrides = {}

    # Verify the response
    assert response.status_code == 200
    report = response.json()
    assert "markdown" in report
    assert "summary_stats" in report
    assert "top_ranked" in report
    assert "scoring_weights" in report

    # Verify the content
    assert report["markdown"] == "# Test Report"
    assert report["summary_stats"] == {"test_stat": "test_value"}
    assert report["top_ranked"] == ["Test Model 1", "Test Model 2"]
    assert report["scoring_weights"]["vram_weight"] == 0.3
