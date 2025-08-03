"""
Schema versioning support for the glyphd API.
"""

from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class SchemaVersion(str, Enum):
    """
    Supported API schema versions.
    
    This enum defines all supported schema versions for the ingestion API,
    enabling backward compatibility and controlled evolution.
    """
    
    V1_0 = "v1.0"
    V1_1 = "v1.1"
    
    @classmethod
    def get_supported_versions(cls) -> List[str]:
        """
        Get list of all supported schema versions.
        
        Returns:
            List of supported version strings
        """
        return [version.value for version in cls]
    
    @classmethod
    def get_default_version(cls) -> str:
        """
        Get the default schema version for new requests.
        
        Returns:
            Default version string
        """
        return cls.V1_1.value
    
    @classmethod
    def is_supported(cls, version: str) -> bool:
        """
        Check if a schema version is supported.
        
        Args:
            version: Version string to check
            
        Returns:
            True if version is supported, False otherwise
        """
        return version in cls.get_supported_versions()


class ImportRequestDTO(BaseModel):
    """
    Base DTO for import requests with schema versioning support.
    
    This DTO can be extended by specific import request types to ensure
    consistent schema versioning across all ingestion endpoints.
    """
    
    schema_version: SchemaVersion = Field(
        default=SchemaVersion.V1_1,
        description="API schema version for this request"
    )
    
    class Config:
        """Pydantic model configuration."""
        
        json_schema_extra = {
            "example": {
                "schema_version": "v1.1"
            }
        }


class SchemaVersionInfo(BaseModel):
    """
    DTO for schema version information endpoint.
    
    Provides information about supported schema versions and their capabilities.
    """
    
    supported_versions: List[str] = Field(..., description="List of supported schema versions")
    default_version: str = Field(..., description="Default schema version for new requests")
    current_version: str = Field(..., description="Latest available schema version")
    
    class Config:
        """Pydantic model configuration."""
        
        json_schema_extra = {
            "example": {
                "supported_versions": ["v1.0", "v1.1"],
                "default_version": "v1.1",
                "current_version": "v1.1"
            }
        }