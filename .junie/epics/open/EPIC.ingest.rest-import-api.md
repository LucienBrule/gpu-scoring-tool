## EPIC: REST Ingestion API

### Overview
This Epic introduces and formalizes the ingestion pathway for scored GPU listing data through the `glyphd` FastAPI service. While CSV ingestion via CLI is stable, this Epic expands support to REST-based ingestion workflows to enable remote data submission, automation pipelines, and system interoperability.

### Goals
- Ingest validated pipeline outputs (scored GPU listings) via POST endpoints
- Assign import metadata for tracking (import ID, import timestamp, session lineage)
- Handle individual row validation and partial failure cases
- Support file-based and JSON body ingestion modes
- Maintain DX and lint/test compliance standards

### Scope
This Epic covers:
- Endpoint definitions and validation for import
- Upload of structured CSV artifacts via form-data or JSON body
- Metadata generation and tracking (import_id, import_index, timestamp)
- Import summary generation and error response design
- Integration with persistence layer (SQLite engine)
- Associated tests (engine-level, route-level, and integration)

### Out of Scope
- Direct ingestion from external web URLs (scraping/importing from the web)
- Authorization or multi-tenant permissioning

### Tasks
- `TASK.ingest.api.import-csv`
- `TASK.ingest.api.import-from-pipeline-output`
- `TASK.ingest.api.upload-and-validate-artifacts`
- `TASK.ingest.api.import-response-format`
- `TASK.ingest.api.schema-versioning-support` (optional/future)

### Constraints
- Must conform to DTO and SQLite schema already defined
- Must provide a unique `import_id` (UUID) per ingest session
- Rows must include an `import_index` (ordinal within import)
- All responses must return a clear summary (count, errors, import_id)

### Success Criteria
- Clients can submit JSON or CSV-formatted scored listings to `glyphd`
- The service accepts, validates, and persists the listings with metadata
- Operators can query data by `import_id` to analyze temporal effects
- Tasks are lint-clean (`ruff`, `flake8`, `black`, `isort`) and test-covered (`pytest`)