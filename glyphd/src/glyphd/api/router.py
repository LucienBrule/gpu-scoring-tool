"""
FastAPI router for the glyphd API.
"""

from fastapi import APIRouter, FastAPI

# Import and include individual routers from their respective modules
from glyphd.api.routes.forecast import router as forecast_router
from glyphd.api.routes.health import router as health_router
from glyphd.api.routes.import_csv import router as import_csv_router
from glyphd.api.routes.import_from_pipeline import router as import_from_pipeline_router
from glyphd.api.routes.listings import router as listings_router
from glyphd.api.routes.ml import router as ml_router
from glyphd.api.routes.models import router as models_router
from glyphd.api.routes.persist import router as persist_router
from glyphd.api.routes.report import router as report_router
from glyphd.api.routes.schema_version import router as schema_version_router
from glyphd.api.routes.upload_artifact import router as upload_artifact_router

# Create the API router
router = APIRouter(prefix="/api")

router.include_router(forecast_router)
router.include_router(health_router)
router.include_router(import_csv_router)
router.include_router(import_from_pipeline_router)
router.include_router(listings_router)
router.include_router(ml_router)
router.include_router(models_router)
router.include_router(persist_router)
router.include_router(report_router)
router.include_router(schema_version_router)
router.include_router(upload_artifact_router)


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: The configured FastAPI application.
    """
    app = FastAPI(
        title="Glyphd: GPU Market API",
        description=(
            "API service exposing enriched GPU listings"
            "model metadata, scoring reports, "
            "and insight overlays from the glyphsieve pipeline."
        ),
        version="0.1.0",
        contact={
            "name": "Glyphsieve Research",
            "url": "https://github.com/lucienbrule/gpu-scoring-tool",
        },
        openapi_tags=[
            {"name": "Listings", "description": "Access enriched GPU listing records"},
            {"name": "ML", "description": "Machine learning GPU classification endpoints"},
            {"name": "Models", "description": "Explore normalized GPU model specs"},
            {"name": "Persist", "description": "Import and persist GPU listings to SQLite store"},
            {"name": "Report", "description": "Retrieve current insight summary and scoring weights"},
            {"name": "Health", "description": "Basic system liveness check"},
        ],
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # Mount the API router
    app.include_router(router)

    return app
