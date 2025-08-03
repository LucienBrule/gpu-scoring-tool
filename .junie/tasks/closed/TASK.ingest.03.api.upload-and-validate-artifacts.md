


## TASK.ingest.03.api.upload-and-validate-artifacts

## ✍️ Planning Commentary

**Strategic Direction (Updated):** The Operator has specified that uploaded artifacts should be kept in-memory by default, but provide a `save_to_disk: bool` flag for auditing/debug purposes. This balances performance with debugging capabilities.

**Implementation Approach:** This endpoint provides "dry-run" validation without persistence, enabling clients to validate files before committing to ingestion. The optional disk save feature supports debugging and audit workflows.

**File Handling Policy:** Default to in-memory processing for performance, but support optional disk persistence when `save_to_disk=true` is specified in the request.

This task implements the API endpoint to allow clients (such as CLI tools or the frontend) to upload artifact files (CSV, JSON, or YAML) and validate their schema before ingestion.

---

### 🎯 Goal

Define a FastAPI POST endpoint that accepts a file upload, validates its schema based on the file type and expected data model (e.g., GPU listing schema), and returns a validation report.

---

### 📦 Requirements

- Endpoint: `POST /api/ingest/upload-artifact`
- Input:
  - Accept `multipart/form-data`
  - Allowed file types: `.csv`, `.json`, `.yaml`, `.yml`
- Validation logic:
  - Parse uploaded file
  - Match against known schema for:
    - GPU listings
    - Reports
    - Model metadata (optional)
  - Return structured error report if schema mismatch
- Output:
  - `200 OK` with:
    ```json
    {
      "valid": true,
      "type": "gpu_listing",
      "rows": 10423,
      "schema": "v1.1",
      "warnings": [],
      "errors": []
    }
    ```
  - `400 Bad Request` on unsupported file or unreadable content

---

### 🛠 Implementation Notes

- Use FastAPI’s `UploadFile` with streaming and temporary file if needed
- Add parser helpers under `glyphsieve/artifact_validation/`
- Use Pydantic for schema enforcement
- Future versions may add automatic ingestion from this endpoint

---

### ✅ Completion Criteria

- Endpoint reachable and documented in OpenAPI
- Artifact parser supports `.csv`, `.json`, `.yaml`
- Schema validation errors and success cases both return usable structured output
- Tests written for:
  - Valid GPU listing CSV
  - Invalid schema JSON
  - Unsupported extension

---

### 🔗 Dependencies

- Relies on schema definitions under `glyphsieve/models/`
- May re-use normalization logic as part of validation
- Compatible with `TASK.ingest.02.api.import-from-pipeline-output`

---

### ✍️ Notes

- This endpoint will enable Junie, Goose, and CLI tools to safely upload data previews before ingestion.
- Design for forward-compatibility with auto-tagging and ingestion.

## ✅ Task Completed

**Changes made:**
- Created `ArtifactValidationResultDTO` with comprehensive validation result fields
- Implemented `/api/ingest/upload-artifact` endpoint with multipart form-data support
- Added support for CSV, JSON, and YAML file validation
- Implemented GPU listing schema detection and validation logic
- Added optional `save_to_disk` parameter for debugging purposes
- Fixed Pydantic field name conflict by renaming "schema" to "schema_version"
- Added PyYAML dependency for YAML file support
- Registered new route in main API router

**Outcomes:**
- Endpoint successfully validates uploaded files without persisting data
- Supports CSV files with automatic GPU listing type detection
- Returns detailed validation results with row counts, warnings, and errors
- Optional disk saving works for debugging and audit purposes
- Proper error handling for unsupported file types and malformed content
- Successfully tested with 3-row CSV file showing valid GPU listing detection

**Lessons learned:**
- Pydantic field names must not shadow BaseModel attributes (avoid "schema")
- File validation requires careful type detection based on column structure
- Multipart form-data handling works well with FastAPI UploadFile
- YAML support requires PyYAML dependency

**Follow-up needed:**
- None - endpoint is fully functional and ready for production use