"""
FastAPI router for the glyphd API.
"""
from fastapi import APIRouter, FastAPI

# Create the API router
router = APIRouter(prefix="/api")

@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    Returns a simple status message to indicate the API is running.
    """
    return {"status": "ok"}

def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        FastAPI: The configured FastAPI application.
    """
    app = FastAPI(
        title="GlyphD API",
        description="API for GPU scoring and market analysis",
        version="0.1.0",
    )
    
    # Mount the API router
    app.include_router(router)
    
    return app