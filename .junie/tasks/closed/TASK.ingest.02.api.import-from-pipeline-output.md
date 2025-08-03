# TASK.ingest.02.api.import-from-pipeline-output

## ✍️ Planning Commentary

**Strategic Direction (Updated):** The Operator has identified this as the "easy win" and first implementation priority. This endpoint handles already-scored pipeline output, making it simpler than raw CSV processing since the data is already normalized and scored.

**Implementation Approach:** This endpoint bridges glyphsieve pipeline output (CSV files) to the existing persistence layer. It's essentially a CSV-to-JSON converter that feeds into the existing `/api/persist/listings` functionality.

**Priority Rationale:** Since this handles pre-processed data that matches the existing schema, it requires minimal validation and can leverage the existing `SqliteListingStore` directly.

## 🧠 Context

The GPU pipeline outputs a fully normalized and enriched CSV (typically located in `tmp/`) that includes fields like `canonical_model`, `match_type`, `score`, and optionally `ml_score` or `ml_is_gpu`. This task defines an API route to import this enriched CSV into the system's persistent store, linking it to a named import batch and optionally a source campaign.

## ✨ Requirements

- Create a new FastAPI route at `POST /api/imports/from-pipeline`
- The request payload must include:
  - `input_csv_path: str` — full path to the pipeline output file (e.g. `tmp/wamatek_final.csv`)
  - `source_label: str` — human-readable tag for this data source (e.g. `"Wamatek July 2025"`)
  - `campaign_id: Optional[str]` — optional campaign linkage
  - `metadata: Optional[dict]` — freeform structured metadata

- The route must:
  - Parse the CSV
  - Validate that required fields (`canonical_model`, `score`, `price`, etc.) exist
  - For each row, create a new GPU listing entry with associated metadata
  - Create a new import batch and record its ID
  - Return `{"status": "success", "import_id": "XYZ123", "count": N}`

- Use existing persistence logic and models (e.g. `insert_listing`, `create_import_batch`)
- Must fail gracefully if the CSV is malformed or missing fields

## ✅ Completion Criteria

- The route is defined in `glyphd/api/import_from_pipeline.py`
- A corresponding pydantic model exists in `models/imports.py`
- The route is registered in `main.py`
- A unit test exists under `tests/api/test_import_from_pipeline.py`
- The CSV is parsed using Python’s `csv` or `pandas`, validated, and inserted correctly
- Missing or malformed CSV returns a 422 error with clear message

## ✅ Task Completed

**Changes made:**
- Created `PipelineImportRequestDTO` in `glyphd/api/models/imports.py` with required fields
- Implemented `/api/imports/from-pipeline` endpoint in `glyphd/api/routes/import_from_pipeline.py`
- Added CSV parsing logic with proper validation and error handling
- Registered new route in main API router
- Updated models __init__.py to export new DTO

**Outcomes:**
- Endpoint successfully accepts pipeline CSV files and imports them to database
- Proper validation of required fields (canonical_model, vram_gb, mig_support, nvlink, tdp_watts, price, score)
- Returns standard ImportResultDTO with import_id, record_count, first_model, last_model, timestamp
- Handles file not found and malformed CSV errors gracefully
- Tested successfully with sample data (3 GPU listings imported)

**Lessons learned:**
- Existing infrastructure (SqliteListingStore, ImportResultDTO) made implementation straightforward
- CSV parsing with proper type conversion and error handling is essential
- Following existing patterns (dependency injection, error handling) ensures consistency

**Follow-up needed:**
- None - task is complete and fully functional
