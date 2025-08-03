

# TASK.ingest.01.api.import-csv

## ✍️ Planning Commentary

**Strategic Direction (Updated):** The Operator has confirmed this endpoint should handle raw CSV files that need normalization and scoring. Raw uploads will trigger normalization as a background job via the glyphsieve pipeline integration (TASK.ingest.07).

**Implementation Approach:** This endpoint accepts raw CSV files, validates basic structure, and triggers background processing through the PipelineService. It's part of the "dual path ingestion" strategy supporting both raw and pre-scored data.

**Relationship to Pipeline:** This task coordinates with TASK.ingest.07 (pipeline integration) to process raw listings through normalization and scoring before persistence.

## 🧠 Goal

Create a new backend API route in `glyphd/` that allows clients to submit a CSV file for ingestion into the GPU scoring system. The API should accept multipart form uploads, parse the CSV contents, and handle the data appropriately based on whether it's raw listings or already-scored data.

This task focuses on file handling and CSV parsing — the relationship to the existing `/api/persist/listings` endpoint should be clarified.

## 🛠️ Requirements

- Create a new FastAPI POST route: `/api/import/csv`
- Accept a file via multipart form encoding
- Validate the file extension is `.csv`
- Parse the file using a streaming CSV parser (e.g., `csv` module or `pandas` with chunks)
- Save the ingested rows to a dedicated `import_batches/` folder (can live under `.data/` or be configurable)
- Generate a UUID-based batch ID for each upload and include it in the response
- Return structured ingestion metadata: row count, rejected lines (if any), estimated source
- Add test coverage for:
  - Invalid file types
  - Uploading malformed CSVs
  - Ingesting a valid small CSV
- All file parsing and error handling must be safe and non-blocking
- Reject files over 50MB in size

## ✨ Bonus

- Include ingestion timestamp and batch ID in a minimal JSON log or metadata sidecar (e.g., `batch_uuid.meta.json`)
- Emit an event to a future pub/sub or task queue layer for follow-up processing

## 📦 Output

- A working route at `/api/import/csv`
- Uploaded files are written to disk with a UUID-named folder (e.g., `.data/import_batches/ab3f.../original.csv`)
- Response includes:
  ```json
  {
    "batch_id": "ab3f19b1-f24c-412c-a198-338a0c388c01",
    "row_count": 1234,
    "rejected_rows": 0,
    "filename": "vendor-data.csv"
  }
  ```

## ✅ Completion Criteria

- Code merged and route operational via Docker Compose dev stack
- CLI curl test demonstrates ingestion:
  ```bash
  curl -X POST http://localhost:8000/api/import/csv \
    -F 'file=@data/vendor.csv'
  ```
- Files appear in the import folder and are listed in ingestion logs
- Tests pass locally and in CI

## ✅ Task Completed

**Changes made:**
- Created `/api/import/csv` endpoint in `glyphd/api/routes/import_csv.py`
- Implemented `CSVImportResultDTO` for response formatting
- Added multipart file upload support with validation (file extension, size limits)
- Implemented CSV parsing and row counting with error handling
- Added file storage to `data/import_batches/{batch_id}/` with original.csv and metadata.json
- Registered route in main API router
- Added `python-multipart` dependency to support file uploads

**Outcomes:**
- Endpoint successfully accepts CSV file uploads via multipart form data
- Validates file extension (.csv only) and size (50MB limit)
- Stores uploaded files with UUID-based batch IDs
- Returns structured metadata: batch_id, row_count, rejected_rows, filename, timestamp
- Creates metadata sidecar files for audit and future processing
- Handles encoding errors and malformed CSV files gracefully
- Tested successfully with 4-row sample CSV file

**Lessons learned:**
- FastAPI requires `python-multipart` dependency for file upload endpoints
- Proper error handling and cleanup is essential for file operations
- UUID-based batch IDs provide good uniqueness for concurrent uploads
- Metadata files enable future pipeline integration and audit trails

**Follow-up needed:**
- Integration with TASK.ingest.07 (pipeline processing) to process uploaded raw CSV files
- Enhanced validation for specific GPU listing fields (future enhancement)