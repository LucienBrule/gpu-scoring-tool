# TASK.daemon.persist.sqlite-store.md

## Title
Persist Scored Listings Using SQLite in glyphd

## Category
daemon

## Status
open

## Purpose
Implement persistent storage for enriched and scored GPU listings, using SQLite. This store will power the API-layer of `glyphd`, enabling structured query surfaces, delta tracking, and future analytics.

This logic **must live in `glyphd` only**. `glyphsieve` must not own or manage persistence. It may communicate with the daemon over HTTP, but never directly own or reimplement storage.

## Requirements

1. **Model Definition**
   - Create SQLAlchemy models in `glyphd.models.sqlite`
   - Mirror the enriched/scored listing DTO from `glyphsieve` (import the shared model if available)
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

3. **Ingestion REST Endpoint**
   - Implement FastAPI POST endpoint `/api/listings/import` in `glyphd.api.router`
   - Endpoint must:
     - Accept multipart form or JSON payload containing the scored CSV file
     - Parse CSV into `EnrichedGPUListingDTO` objects
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

## Completion Criteria
- The SQLite DB can be created, queried, and populated via the REST endpoints
- GET `/api/listings` returns correct JSON for sample data
- REST ingestion endpoint `/api/listings/import` successfully imports listings from CSV
- Docker Compose runs glyphd on port 8080 without ad-hoc commands
- Unit and integration tests (including REST client tests) cover storage and endpoints
- All linting and formatting commands complete without errors

## Persona
You are the Archivist of glyphd. Your job is to ensure no listing is lost to time, and every scoring event can be reconstructed. Your database is a living memory of the market.

## DX Runbook
```bash
# Start services
docker-compose up -d --build

# Ingest sample CSV via REST
curl -X POST http://localhost:8080/api/listings/import \
  -F "file=@sample/scored_sample.csv" \
  -H "Accept: application/json"

# Query persisted listings
curl "http://localhost:8080/api/listings?model=RTX_A6000&min_score=0.8"

# Run tests (includes unit and REST endpoint tests)
pytest

# Linting & formatting
uv run black glyphd/src
uv run isort glyphd/src
uv run ruff check glyphd/src
uv run flake8 glyphd/src

## Dependency Setup Notes
- You must use `uv` to install all Python dependencies:
  - From within the `glyphd` project directory, run:
    ```bash
    uv add sqlalchemy
    uv add aiosqlite
    uv add pydantic[email]  # if needed for validation, optional
    ```
  - Then, from the monorepo root, run:
    ```bash
    uv sync --all-packages --all-extras
    ```
  - Never use `pip install` directly; this project uses `uv` for reproducibility and monorepo consistency.
```