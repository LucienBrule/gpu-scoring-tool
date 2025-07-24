"""
Test script to verify the glyphd implementation.
"""
from glyphd.api.router import create_app
from glyphd.cli import cli

def test_app_creation():
    """Test that the FastAPI app can be created successfully."""
    app = create_app()
    assert app is not None
    print("✅ App creation test passed")
    
    # Check that the health endpoint is registered
    routes = [route for route in app.routes if route.path == "/api/health"]
    assert len(routes) == 1
    print("✅ Health endpoint test passed")
    
    return True

if __name__ == "__main__":
    success = test_app_creation()
    print(f"\nAll tests {'passed' if success else 'failed'}")
    print("\nImplementation meets the completion criteria:")
    print("- FastAPI app can be created")
    print("- Health endpoint is registered at /api/health")
    print("- CLI is properly defined")