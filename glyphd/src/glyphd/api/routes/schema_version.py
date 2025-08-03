"""
FastAPI route for schema version information.
"""

import logging

from fastapi import APIRouter

from glyphd.api.models import SchemaVersion, SchemaVersionInfo

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/schema",
    tags=["Schema"],
)


@router.get(
    "/versions",
    response_model=SchemaVersionInfo,
    summary="Get supported schema versions",
    description="Retrieve information about supported API schema versions and defaults",
)
def get_schema_versions() -> SchemaVersionInfo:
    """
    Get information about supported API schema versions.
    
    Returns:
        SchemaVersionInfo: Information about supported versions and defaults
    """
    supported_versions = SchemaVersion.get_supported_versions()
    default_version = SchemaVersion.get_default_version()
    current_version = supported_versions[-1]  # Latest version
    
    logger.info(f"Schema version info requested: {len(supported_versions)} versions supported")
    
    return SchemaVersionInfo(
        supported_versions=supported_versions,
        default_version=default_version,
        current_version=current_version,
    )


@router.get(
    "/versions/{version}",
    summary="Check if schema version is supported",
    description="Check if a specific schema version is supported by the API",
)
def check_schema_version(version: str) -> dict:
    """
    Check if a specific schema version is supported.
    
    Args:
        version: Schema version to check (e.g., "v1.1")
        
    Returns:
        Dictionary with version support information
    """
    is_supported = SchemaVersion.is_supported(version)
    
    logger.info(f"Schema version check for '{version}': supported={is_supported}")
    
    return {
        "version": version,
        "supported": is_supported,
        "message": f"Schema version '{version}' is {'supported' if is_supported else 'not supported'}",
        "supported_versions": SchemaVersion.get_supported_versions() if not is_supported else None,
    }