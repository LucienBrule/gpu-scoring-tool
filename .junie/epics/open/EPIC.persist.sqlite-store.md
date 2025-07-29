# EPIC.persist.sqlite-store.md

## Title
Persist Scored Listings Using SQLite in glyphd

## Category
daemon

## Status
open

## Purpose
Implement persistent storage for enriched and scored GPU listings, using SQLite. This store will power the API-layer of `glyphd`, enabling structured query surfaces, delta tracking, and future analytics.

This logic **must live in `glyphd` only**. `glyphsieve` must not own or manage persistence. It may communicate with the daemon over HTTP, but never directly own or reimplement storage.

## Epic Workflow
This epic coordinates multiple related tasks that together implement persistent storage and API endpoints for GPU listings in `glyphd`. The individual tasks are located in `.junie/tasks/open/` and should be completed sequentially. Each task must be closed individually once its scope is finished. Upon completion of each task, update this epic’s status and notes to reflect progress and integration. The flow ensures incremental delivery from schema definition through engine implementation, API endpoints, and testing.

## Tasks in this Epic
- [TASK.persist.01.sqlite-schema-definition.md](.junie/tasks/open/TASK.persist.01.sqlite-schema-definition.md)
- [TASK.persist.02.sqlite-engine-storage.md](.junie/tasks/open/TASK.persist.02.sqlite-engine-storage.md)
- [TASK.persist.03.api.import-listings-endpoint.md](.junie/tasks/open/TASK.persist.03.api.import-listings-endpoint.md)
- [TASK.persist.04.api.query-listings-endpoint.md](.junie/tasks/open/TASK.persist.04.api.query-listings-endpoint.md)
- [TASK.persist.05.tests.sqlite-rest-integration.md](.junie/tasks/open/TASK.persist.05.tests.sqlite-rest-integration.md)
- [TASK.persist.06.metadata.import-id-versioning.md](.junie/tasks/open/TASK.persist.06.metadata.import-id-versioning.md)

## Requirements

1. **Model Definition**
   - Create SQLAlchemy models in `glyphd.models.sqlite`
   - Mirror the enriched/scored listing DTO from `glyphsieve` (import the shared model if available)  
     You may import this DTO directly from `glyphsieve`, but must wrap it in a glyphd-local adapter if mutation or versioning is required.
    - Ensure schema fields include:
      - `model`, `price_usd`, `condition`, `quantity`, `min_order_qty`, `seller`, `region`
      - `vram_gb`, `mig_capable`, `score`, `heuristics`, `seen_at`
      - `source_url`, `source_type`
    - Use a declarative base or ORM-compatible schema
    - Support serialization via Pydantic DTOs (bidirectional mapping)

2. **Engine Setup**
   - Create `glyphd.core.storage.sqlite` or similar
   - Initialize DB at `data/gpu.sqlite` by default
   - Allow override via CLI or env var: `--db-path` or `GLYPHD_DB_PATH`
   - Include create table, upsert listing, and read/query functions
   - Define a helper method `get_sqlite_path()` in `glyphd.config` that resolves the DB path from CLI/env/default. Use this in tests and application bootstrap.

3. **Ingestion REST Endpoint**
   - Implement FastAPI POST endpoint `/api/listings/import` in `glyphd.api.router`
   - Endpoint must:
     - Accept **multipart form with CSV payload** only. JSON ingestion may be added later but is not required.
     - Parse CSV into `EnrichedGPUListingDTO` objects  
       Rows that fail validation must be rejected with a 422 response. Partial ingestion is not supported.
     - Validate schema
     - Insert or update listings in SQLite via the storage layer
   - Do **not** add CLI commands for ingestion; all ingestion is via HTTP

4. **Query REST Endpoint**
   - Implement FastAPI GET endpoint `/api/listings` with query parameters:
     - `model: str`
     - `min_score: float` (optional)
     - `region: str` (optional)
     - `after: datetime` (optional, ISO 8601)
   - Endpoint returns JSON array of persisted listings matching filters
   - Responses must include all persisted fields, including `seen_at`

5. **Testing**
   - Unit test storage engine functions
   - Integration test ingest/query CLI flow with temporary DB file

## Bonus
- Add `schema_version` and `import_id` fields to each row
- Implement migration detection if schema changes in future
- If `import_id` is reused, the corresponding rows should be replaced (idempotent import behavior).

## Completion Criteria
- All tasks listed under this epic (Tasks 01 through 06) are completed and closed.
- The SQLite DB can be created, queried, and populated via the REST endpoints.
- GET `/api/listings` returns correct JSON for sample data.
- REST ingestion endpoint `/api/listings/import` successfully imports listings from CSV.
- Docker Compose runs `glyphd` on port 8080 without ad-hoc commands.
- Unit and integration tests (including REST client tests) cover storage and endpoints and pass successfully.
- All linting and formatting commands complete without errors.