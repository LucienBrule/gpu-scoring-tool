"""
DTO models for import metadata.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from glyphd.api.models.schema_version import SchemaVersion


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


class PipelineImportRequestDTO(BaseModel):
    """
    Data Transfer Object for pipeline import requests.

    Represents a request to import enriched CSV from glyphsieve pipeline output.
    """

    input_csv_path: str = Field(..., description="Full path to the pipeline output file")
    source_label: str = Field(..., description="Human-readable tag for this data source")
    campaign_id: Optional[str] = Field(None, description="Optional campaign linkage")
    metadata: Optional[Dict[str, str]] = Field(None, description="Freeform structured metadata")

    class Config:
        """Pydantic model configuration."""

        json_schema_extra = {
            "example": {
                "input_csv_path": "tmp/wamatek_final.csv",
                "source_label": "Wamatek July 2025",
                "campaign_id": "wamatek-q3-2025",
                "metadata": {"region": "US", "vendor": "wamatek"}
            }
        }


class RowErrorDTO(BaseModel):
    """
    Data Transfer Object for row-level error information.

    Represents detailed error information for a specific row that failed validation.
    """

    row_index: int = Field(..., description="Zero-based index of the row in the input")
    row_data: Dict[str, Any] = Field(..., description="Original row data that failed validation")
    errors: List[str] = Field(..., description="List of specific validation errors for this row")
    field_errors: Dict[str, str] = Field(default_factory=dict, description="Field-specific error messages")

    class Config:
        """Pydantic model configuration."""

        json_schema_extra = {
            "example": {
                "row_index": 5,
                "row_data": {"canonical_model": "InvalidGPU", "price": "not_a_number"},
                "errors": ["Invalid canonical_model format", "Price must be a number"],
                "field_errors": {"price": "Expected float, got string"}
            }
        }


class ImportSummaryStatsDTO(BaseModel):
    """
    Data Transfer Object for import summary statistics.

    Represents aggregate statistics about an import operation.
    """

    total_rows: int = Field(..., description="Total number of rows processed")
    successful_rows: int = Field(..., description="Number of rows successfully imported")
    failed_rows: int = Field(..., description="Number of rows that failed validation")
    warnings_count: int = Field(default=0, description="Number of non-fatal warnings generated")
    processing_time_ms: int = Field(..., description="Total processing time in milliseconds")

    class Config:
        """Pydantic model configuration."""

        json_schema_extra = {
            "example": {
                "total_rows": 100,
                "successful_rows": 95,
                "failed_rows": 5,
                "warnings_count": 2,
                "processing_time_ms": 1250
            }
        }


class ImportResultDTO(BaseModel):
    """
    Data Transfer Object for import operation results.

    Represents the result of an import operation with metadata and error reporting.
    """

    # Core import metadata (existing fields)
    import_id: UUID = Field(..., description="Unique identifier for the import batch")
    record_count: int = Field(..., description="Number of records imported")
    first_model: str = Field(..., description="First model name in the imported batch")
    last_model: str = Field(..., description="Last model name in the imported batch")
    timestamp: datetime = Field(..., description="Timestamp when the import was completed")
    
    # Enhanced error reporting fields (optional for backward compatibility)
    rows_with_errors: Optional[List[RowErrorDTO]] = Field(
        default_factory=list, 
        description="Detailed information about failed rows"
    )
    summary_stats: Optional[ImportSummaryStatsDTO] = Field(
        None, 
        description="Aggregate statistics about the import"
    )
    validation_errors: Optional[List[str]] = Field(
        default_factory=list, 
        description="File-level validation errors"
    )
    warnings: Optional[List[str]] = Field(
        default_factory=list, 
        description="Non-fatal issues that didn't prevent import"
    )
    
    # Additional fields from TASK.ingest.04 requirements
    filename: Optional[str] = Field(None, description="Name of the imported file")
    total_rows: Optional[int] = Field(None, description="Total number of rows processed")
    valid_rows: Optional[int] = Field(None, description="Number of valid rows")
    invalid_rows: Optional[int] = Field(None, description="Number of invalid rows")
    score_range: Optional[tuple[float, float]] = Field(None, description="Range of scores in the import")
    top_models: Optional[List[str]] = Field(default_factory=list, description="Most common models in the import")
    
    # Schema versioning support
    schema_version: SchemaVersion = Field(
        default=SchemaVersion.V1_1,
        description="API schema version for this response"
    )

    class Config:
        """Pydantic model configuration."""

        json_schema_extra = {
            "example": {
                "import_id": "550e8400-e29b-41d4-a716-446655440000",
                "record_count": 3,
                "first_model": "H100_PCIE_80GB",
                "last_model": "A100_SXM4_80GB",
                "timestamp": "2025-07-29T12:12:00",
                "filename": "pipeline_output.csv",
                "total_rows": 5,
                "valid_rows": 3,
                "invalid_rows": 2,
                "score_range": [0.65, 0.85],
                "top_models": ["H100_PCIE_80GB", "A100_SXM4_80GB"],
                "rows_with_errors": [],
                "summary_stats": {
                    "total_rows": 5,
                    "successful_rows": 3,
                    "failed_rows": 2,
                    "warnings_count": 0,
                    "processing_time_ms": 150
                },
                "validation_errors": [],
                "warnings": [],
                "schema_version": "v1.1"
            }
        }


class ArtifactValidationResultDTO(BaseModel):
    """
    Data Transfer Object for artifact validation results.

    Represents the result of validating an uploaded file without persisting it.
    """

    valid: bool = Field(..., description="Whether the artifact passed validation")
    type: str = Field(..., description="Detected artifact type (e.g., 'gpu_listing', 'report')")
    rows: Optional[int] = Field(None, description="Number of rows/records in the artifact")
    schema_version: str = Field(..., description="Schema version used for validation")
    warnings: List[str] = Field(default_factory=list, description="Non-fatal validation warnings")
    errors: List[str] = Field(default_factory=list, description="Validation errors that caused failure")
    filename: Optional[str] = Field(None, description="Original filename of the uploaded artifact")
    file_size: Optional[int] = Field(None, description="Size of the uploaded file in bytes")
    saved_to_disk: bool = Field(default=False, description="Whether the file was saved to disk for debugging")
    saved_path: Optional[str] = Field(None, description="Path where the file was saved (if saved_to_disk=True)")

    class Config:
        """Pydantic model configuration."""

        json_schema_extra = {
            "example": {
                "valid": True,
                "type": "gpu_listing",
                "rows": 150,
                "schema_version": "v1.1",
                "warnings": ["Missing optional field 'condition' in 5 rows"],
                "errors": [],
                "filename": "gpu_listings.csv",
                "file_size": 12345,
                "saved_to_disk": False,
                "saved_path": None
            }
        }
