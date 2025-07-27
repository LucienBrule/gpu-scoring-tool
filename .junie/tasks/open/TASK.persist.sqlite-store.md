

# TASK.persist.sqlite-store.md

## Title
Implement SQLite-backed Persistence for Scored Listings

## Category
persist

## Status
open

## Purpose
Introduce a persistent store to record enriched and scored GPU listings. This will replace or augment CSV outputs with structured, queryable data. It prepares the stack for historical tracking, web views, and delta analysis.

## Requirements

1. **Model Definition**
   - Create SQLAlchemy models that mirror the enriched/scored listing DTO
   - Ensure schema fields include:
     - `model`, `price_usd`, `condition`, `quantity`, `min_order_qty`, `seller`, `region`
     - `vram_gb`, `mig_capable`, `score`, `heuristics`, `seen_at`
     - `source_url`, `source_type`
   - Use a declarative base or ORM-compatible schema
   - Support serialization via Pydantic DTOs (bidirectional mapping)

2. **Engine Setup**
   - Add a storage layer to `glyphsieve.services.sqlite`
   - Initialize the DB at a configurable path (e.g. `data/gpu.sqlite`)
   - Include basic create, upsert, and read APIs

3. **Ingestion Pipeline**
   - Add a CLI command: `glyphsieve ingest --input scored.csv`
   - This should parse scored output, validate rows, and insert them into SQLite

4. **Query Surface**
   - Add CLI command: `glyphsieve query --model RTX_A6000` (or similar)
   - Support filters like `--after`, `--min-score`, or `--region`
   - Format output as table or JSON

5. **Testing**
   - Unit test storage engine functions
   - Integration test ingest/query CLI flow with temporary DB file

## Bonus
- Add `schema_version` and `import_id` fields to each row
- Implement migration detection if schema changes in future

## Completion Criteria
- The SQLite DB can be created, queried, and populated from real scored CSVs
- Queries return filtered results by model, score, or region
- DB interactions are covered by tests
- CLI is updated to include `ingest` and `query` commands