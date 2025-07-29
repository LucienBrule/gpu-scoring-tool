"""
DTO models for import metadata.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ImportMetadata(BaseModel):
    """
    Data Transfer Object for import batch metadata.

    Represents an import batch with its metadata.
    """

    import_id: str = Field(..., description="Unique identifier for the import batch")
    imported_at: datetime = Field(..., description="Timestamp when the import was created")
    source: Optional[str] = Field(None, description="Source of the import (e.g., 'csv', 'api')")
    record_count: int = Field(0, description="Number of records in this batch")
    description: Optional[str] = Field(None, description="Optional description of the import")

    class Config:
        """Pydantic model configuration."""

        json_schema_extra = {
            "example": {
                "import_id": "2025-07-29-batch1",
                "imported_at": "2025-07-29T11:47:00",
                "source": "csv",
                "record_count": 100,
                "description": "Initial import of GPU listings",
            }
        }


class ImportResultDTO(BaseModel):
    """
    Data Transfer Object for import operation results.

    Represents the result of an import operation with metadata.
    """

    import_id: UUID = Field(..., description="Unique identifier for the import batch")
    record_count: int = Field(..., description="Number of records imported")
    first_model: str = Field(..., description="First model name in the imported batch")
    last_model: str = Field(..., description="Last model name in the imported batch")
    timestamp: datetime = Field(..., description="Timestamp when the import was completed")

    class Config:
        """Pydantic model configuration."""

        json_schema_extra = {
            "example": {
                "import_id": "550e8400-e29b-41d4-a716-446655440000",
                "record_count": 3,
                "first_model": "H100_PCIE_80GB",
                "last_model": "A100_SXM4_80GB",
                "timestamp": "2025-07-29T12:12:00",
            }
        }
