"""
FastAPI route for uploading and validating artifacts without persistence.
"""

import csv
import json
import logging
import uuid
from pathlib import Path
from typing import Any, Dict, List

import yaml
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import ValidationError

from glyphd.api.models import ArtifactValidationResultDTO, GPUListingDTO

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/ingest",
    tags=["Validation"],
)

# Configuration
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
VALIDATION_DIR = Path("data/validation")
SUPPORTED_EXTENSIONS = {".csv", ".json", ".yaml", ".yml"}


@router.post(
    "/upload-artifact",
    response_model=ArtifactValidationResultDTO,
    summary="Upload and validate artifact file",
    description="Upload a file (CSV, JSON, or YAML) and validate its schema without persisting the data",
)
async def upload_artifact(
    file: UploadFile = File(..., description="Artifact file to validate"),
    save_to_disk: bool = Form(False, description="Whether to save the file to disk for debugging"),
) -> ArtifactValidationResultDTO:
    """
    Upload and validate an artifact file without persisting the data.
    
    Args:
        file: Uploaded artifact file
        save_to_disk: Whether to save the file to disk for debugging
        
    Returns:
        ArtifactValidationResultDTO: Validation results and metadata
        
    Raises:
        HTTPException: If file validation fails or unsupported file type
    """
    # Validate file extension
    if not file.filename:
        raise HTTPException(
            status_code=422,
            detail="Filename is required"
        )
    
    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=422,
            detail=f"Unsupported file type. Supported extensions: {', '.join(SUPPORTED_EXTENSIONS)}"
        )
    
    # Check file size
    if file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {MAX_FILE_SIZE // (1024*1024)}MB."
        )
    
    try:
        # Read file content
        content = await file.read()
        file_size = len(content)
        
        # Initialize validation result
        validation_result = ArtifactValidationResultDTO(
            valid=False,
            type="unknown",
            schema_version="v1.1",
            filename=file.filename,
            file_size=file_size,
            saved_to_disk=False,
        )
        
        # Save to disk if requested
        saved_path = None
        if save_to_disk:
            saved_path = await _save_file_to_disk(file.filename, content)
            validation_result.saved_to_disk = True
            validation_result.saved_path = str(saved_path)
        
        # Validate based on file type
        if file_extension == ".csv":
            validation_result = await _validate_csv_artifact(content, validation_result)
        elif file_extension == ".json":
            validation_result = await _validate_json_artifact(content, validation_result)
        elif file_extension in {".yaml", ".yml"}:
            validation_result = await _validate_yaml_artifact(content, validation_result)
        
        logger.info(
            f"Validated artifact '{file.filename}': "
            f"valid={validation_result.valid}, type={validation_result.type}, "
            f"rows={validation_result.rows}, errors={len(validation_result.errors)}"
        )
        
        return validation_result
        
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=422,
            detail="Invalid file encoding. Please ensure the file is UTF-8 encoded."
        )
    except Exception as e:
        logger.error(f"Failed to validate artifact '{file.filename}': {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to validate artifact: {e!s}"
        )


async def _save_file_to_disk(filename: str, content: bytes) -> Path:
    """
    Save uploaded file to disk for debugging purposes.
    
    Args:
        filename: Original filename
        content: File content as bytes
        
    Returns:
        Path to saved file
    """
    # Create validation directory
    VALIDATION_DIR.mkdir(parents=True, exist_ok=True)
    
    # Generate unique filename to avoid conflicts
    unique_id = str(uuid.uuid4())[:8]
    safe_filename = f"{unique_id}_{filename}"
    file_path = VALIDATION_DIR / safe_filename
    
    # Write file
    with open(file_path, 'wb') as f:
        f.write(content)
    
    logger.info(f"Saved validation file to: {file_path}")
    return file_path


async def _validate_csv_artifact(content: bytes, result: ArtifactValidationResultDTO) -> ArtifactValidationResultDTO:
    """
    Validate CSV artifact for GPU listing schema.
    
    Args:
        content: CSV file content as bytes
        result: Validation result to update
        
    Returns:
        Updated validation result
    """
    try:
        csv_content = content.decode('utf-8')
        
        # Parse CSV
        reader = csv.DictReader(csv_content.splitlines())
        
        if not reader.fieldnames:
            result.errors.append("CSV file has no header row")
            return result
        
        # Count rows and validate structure
        rows = list(reader)
        result.rows = len(rows)
        
        if not rows:
            result.errors.append("CSV file contains no data rows")
            return result
        
        # Detect artifact type based on columns
        fieldnames = set(reader.fieldnames)
        
        # Check for GPU listing schema
        gpu_listing_fields = {"title", "price"}
        scored_gpu_fields = {"canonical_model", "vram_gb", "score"}
        
        if gpu_listing_fields.issubset(fieldnames):
            result.type = "gpu_listing"
            result = await _validate_gpu_listing_rows(rows, result)
        elif scored_gpu_fields.issubset(fieldnames):
            result.type = "scored_gpu_listing"
            result = await _validate_scored_gpu_rows(rows, result)
        else:
            result.type = "unknown"
            result.warnings.append(f"Could not determine artifact type from columns: {list(fieldnames)}")
        
        # Mark as valid if no errors
        result.valid = len(result.errors) == 0
        
        return result
        
    except UnicodeDecodeError:
        result.errors.append("Invalid CSV encoding")
        return result
    except csv.Error as e:
        result.errors.append(f"Malformed CSV file: {e}")
        return result
    except Exception as e:
        result.errors.append(f"CSV validation error: {e}")
        return result


async def _validate_json_artifact(content: bytes, result: ArtifactValidationResultDTO) -> ArtifactValidationResultDTO:
    """
    Validate JSON artifact for known schemas.
    
    Args:
        content: JSON file content as bytes
        result: Validation result to update
        
    Returns:
        Updated validation result
    """
    try:
        json_content = content.decode('utf-8')
        data = json.loads(json_content)
        
        # Handle different JSON structures
        if isinstance(data, list):
            result.rows = len(data)
            if data and isinstance(data[0], dict):
                # Try to validate as GPU listing array
                result = await _validate_json_gpu_listings(data, result)
            else:
                result.type = "array"
                result.warnings.append("JSON array detected but could not determine item type")
        elif isinstance(data, dict):
            result.rows = 1
            result.type = "object"
            result.warnings.append("Single JSON object detected - validation limited")
        else:
            result.errors.append("JSON must contain an object or array")
            return result
        
        # Mark as valid if no errors
        result.valid = len(result.errors) == 0
        
        return result
        
    except UnicodeDecodeError:
        result.errors.append("Invalid JSON encoding")
        return result
    except json.JSONDecodeError as e:
        result.errors.append(f"Malformed JSON file: {e}")
        return result
    except Exception as e:
        result.errors.append(f"JSON validation error: {e}")
        return result


async def _validate_yaml_artifact(content: bytes, result: ArtifactValidationResultDTO) -> ArtifactValidationResultDTO:
    """
    Validate YAML artifact for known schemas.
    
    Args:
        content: YAML file content as bytes
        result: Validation result to update
        
    Returns:
        Updated validation result
    """
    try:
        yaml_content = content.decode('utf-8')
        data = yaml.safe_load(yaml_content)
        
        # Handle different YAML structures
        if isinstance(data, list):
            result.rows = len(data)
            result.type = "array"
            result.warnings.append("YAML array detected - limited validation available")
        elif isinstance(data, dict):
            result.rows = 1
            result.type = "object"
            result.warnings.append("YAML object detected - limited validation available")
        else:
            result.errors.append("YAML must contain an object or array")
            return result
        
        # Mark as valid if no errors
        result.valid = len(result.errors) == 0
        
        return result
        
    except UnicodeDecodeError:
        result.errors.append("Invalid YAML encoding")
        return result
    except yaml.YAMLError as e:
        result.errors.append(f"Malformed YAML file: {e}")
        return result
    except Exception as e:
        result.errors.append(f"YAML validation error: {e}")
        return result


async def _validate_gpu_listing_rows(rows: List[Dict[str, Any]], result: ArtifactValidationResultDTO) -> ArtifactValidationResultDTO:
    """
    Validate raw GPU listing rows.
    
    Args:
        rows: List of CSV row dictionaries
        result: Validation result to update
        
    Returns:
        Updated validation result
    """
    required_fields = {"title", "price"}
    
    for i, row in enumerate(rows):
        # Check required fields
        missing_fields = required_fields - set(row.keys())
        if missing_fields:
            result.errors.append(f"Row {i+1}: Missing required fields: {missing_fields}")
            continue
        
        # Validate price field
        try:
            price = float(row.get("price", 0))
            if price <= 0:
                result.warnings.append(f"Row {i+1}: Price should be positive, got {price}")
        except (ValueError, TypeError):
            result.errors.append(f"Row {i+1}: Invalid price value: {row.get('price')}")
        
        # Check for empty title
        if not row.get("title", "").strip():
            result.errors.append(f"Row {i+1}: Title cannot be empty")
    
    return result


async def _validate_scored_gpu_rows(rows: List[Dict[str, Any]], result: ArtifactValidationResultDTO) -> ArtifactValidationResultDTO:
    """
    Validate scored GPU listing rows.
    
    Args:
        rows: List of CSV row dictionaries
        result: Validation result to update
        
    Returns:
        Updated validation result
    """
    required_fields = {"canonical_model", "vram_gb", "score", "price"}
    
    for i, row in enumerate(rows):
        # Check required fields
        missing_fields = required_fields - set(row.keys())
        if missing_fields:
            result.errors.append(f"Row {i+1}: Missing required fields: {missing_fields}")
            continue
        
        # Validate numeric fields
        numeric_fields = {"vram_gb", "score", "price"}
        for field in numeric_fields:
            try:
                value = float(row.get(field, 0))
                if field == "score" and not (0 <= value <= 100):
                    result.warnings.append(f"Row {i+1}: Score should be 0-100, got {value}")
            except (ValueError, TypeError):
                result.errors.append(f"Row {i+1}: Invalid {field} value: {row.get(field)}")
    
    return result


async def _validate_json_gpu_listings(data: List[Dict[str, Any]], result: ArtifactValidationResultDTO) -> ArtifactValidationResultDTO:
    """
    Validate JSON array as GPU listings.
    
    Args:
        data: List of JSON objects
        result: Validation result to update
        
    Returns:
        Updated validation result
    """
    try:
        # Try to validate each item as GPUListingDTO
        valid_count = 0
        for i, item in enumerate(data):
            try:
                GPUListingDTO(**item)
                valid_count += 1
            except ValidationError as e:
                result.errors.append(f"Item {i+1}: {e}")
        
        if valid_count > 0:
            result.type = "gpu_listing"
            if valid_count < len(data):
                result.warnings.append(f"Only {valid_count}/{len(data)} items passed validation")
        else:
            result.type = "unknown"
            result.errors.append("No items matched GPU listing schema")
        
        return result
        
    except Exception as e:
        result.errors.append(f"JSON GPU listing validation error: {e}")
        return result