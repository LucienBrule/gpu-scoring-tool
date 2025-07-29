# TASK.persist.03.api.import-listings-endpoint

## Title
Implement REST Endpoint to Import Scored Listings into SQLite Store

## Epic Link
[EPIC.persist.sqlite-store](../epics/open/EPIC.persist.sqlite-store.md)

## Dependencies
- [TASK.persist.01.sqlite-schema-definition](../tasks/open/TASK.persist.01.sqlite-schema-definition.md)
- [TASK.persist.02.sqlite-engine-storage](../tasks/open/TASK.persist.02.sqlite-engine-storage.md)

## Context
Following schema creation (TASK.persist.01) and storage engine implementation (TASK.persist.02), this task adds a dedicated REST endpoint for ingesting scored listing data into the SQLite store. The source of the data is the final stage output of the glyphsieve pipeline (`final_score` + metadata). This endpoint will serve as the entry point for appending new records to the listings table.

## Requirements

### Endpoint Definition
- Path: `POST /api/persist/listings`
- Accepts: JSON array of listing records, each conforming to `GPUListingDTO`
- Behavior:
  - Validates the request body using FastAPI + Pydantic.
  - Assigns a UUID import session ID to the batch.
  - Writes all valid listings into the `gpu_listings` table.
  - Returns: `ImportResultDTO` containing:
    - `import_id: UUID`
    - `record_count: int`
    - `first_model: str`
    - `last_model: str`
    - `timestamp: datetime`
  - Returns metadata about the import (e.g., count, UUID, first/last model, timestamp).

### Integration
- Uses the engine and session logic from `SQLiteStorageEngine`.
- Leverages the DTO → ORM model conversion logic defined in the previous task.
- Any failed records should return a 422 with descriptive validation errors.

### Implementation Notes
- Use dependency injection for the storage backend via `Depends(get_storage_engine)`.
- Log each import event using a structured logger if available.
- Ensure CORS is not required for this endpoint.
- Validate against duplicate import ID collisions (UUID should be unique).

## Response Model
Define a Pydantic model `ImportResultDTO` with:
- `import_id: UUID`
- `record_count: int`
- `first_model: str`
- `last_model: str`
- `timestamp: datetime`

## Developer DX

### Local Testing
- `uvicorn glyphd:app --reload`
- POST test data using `curl`, HTTPie, or Python script.
- Validate written rows via temporary debug route or by running scripted sqlite3 queries in non-interactive batch mode.
- Run unit and integration tests: `pytest tests/test_api_persist.py::test_import_endpoint`

### Test Input Example
```json
[
  {
    "model": "H100_PCIE_80GB",
    "price": 34995.0,
    "score": 0.92,
    "listing_source": "ServerSupply.com",
    "import_id": "auto-generated"
  }
]
```

## Acceptance Criteria
- [ ] Endpoint is reachable at `POST /api/persist/listings`
- [ ] Valid JSON payloads of `GPUListingDTO` array are accepted and persisted
- [ ] A unique `import_id` is generated and returned
- [ ] Response conforms to `ImportResultDTO`
- [ ] Records are committed to the `gpu_listings` table
- [ ] Invalid payloads return HTTP 422 with detailed errors
- [ ] Covered by `tests/test_api_persist.py::test_import_endpoint`
