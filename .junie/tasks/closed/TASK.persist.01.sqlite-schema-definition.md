# TASK.persist.01.sqlite-schema-definition

## Title
Define Initial SQLite Schema for Listings & Models

## Epic
[EPIC.persist.sqlite-store](../../epics/open/EPIC.persist.sqlite-store.md)

## Status
Closed

## Context
This schema design reflects a strategic architectural decision to separate domain boundaries clearly, removing embedded resource loaders to simplify the persistence layer. It marks a key integration milestone aligning with our version tagging strategy to ensure smooth incremental adoption and backward compatibility.

## Purpose
Establish the foundational SQLite schema required to persist enriched and scored GPU listings, as well as static GPU model metadata. This schema will serve as the persistent backing store for all future API queries and analytics.

## Goals

- Define schema that supports the following tables:
  - `listings`: Raw listing metadata (parsed from CSV input)
  - `models`: Normalized GPU model registry (e.g., `canonical_model`)
  - `scored_listings`: Enrichment and scoring outputs (VRAM, TDP, MIG, score, weights)
  - `quantized_listings` (optional): Quantization capacities if present

- Ensure compatibility with DTOs already defined in:
  - `ListingDTO`
  - `GPUModelDTO`
  - `ScoredListingDTO`
  - `QuantizedListingDTO` (if separated)

- Define schema for GPU model registry (denormalized for query efficiency).

- Allow import versioning and timestamping of batches for differential updates later.

## Deliverables

- SQL schema definition (can be expressed via SQLAlchemy or raw `.sql` file)
- Markdown spec showing schema layout for review
- Sanity-checked via `sqlite3` CLI or automated test
- Table/column-level comments encouraged
- A SQLAlchemy-based migration stub (`alembic/env.py` & versions) in addition to raw SQL
- A sample Python test harness to verify schema (e.g., `tests/test_schema.py`)

## Acceptance Criteria

- [x] Schema written and committed under `glyphd/sqlite/schema.sql` or equivalent
- [x] All primary/foreign keys defined where applicable
- [x] Can be instantiated via CLI or Python code without error
- [x] Reviewed for extensibility (e.g., can we support new score fields?)
- [x] Reviewed for query performance (e.g., indexes on `canonical_model`, `score`)
- [x] CI pipeline can instantiate schema on a fresh database
- [x] Migration scripts included under `glyphd/sqlite/migrations`

## Developer Workflow

Run the following to test schema instantiation and verification:

```bash
# Instantiate schema
uv run -m glyphd init-db --db-path data/gpu.db
# Run schema tests
pytest tests/test_schema.py
```

## Notes

- Do NOT include listing source data (e.g. seller name, URL) in this schema unless explicitly required. Focus is on GPU model + score metadata.
- Future migration support is out of scope but should be considered in naming and structure.

## Related Tasks

- [TASK.persist.02.sqlite-engine-storage.md](../open/TASK.persist.02.sqlite-engine-storage.md)
- [TASK.persist.03.api.import-listings-endpoint.md](../open/TASK.persist.03.api.import-listings-endpoint.md)

## Implementation Notes

- Plan for future migrations using Alembic with versioned scripts under `glyphd/sqlite/migrations`.
- Use version tags and batch timestamps to manage schema evolution and differential data imports.
- Maintain backward compatibility by careful schema extension and deprecation strategies.

## ✅ Task Completed

**Changes made:**
- Created SQLite schema definition in `glyphd/src/glyphd/sqlite/schema.sql` with tables for:
  - `schema_version`: For tracking schema versions and migrations
  - `import_batches`: For tracking import batches and enabling differential updates
  - `models`: For storing normalized GPU model registry with technical specifications
  - `listings`: For storing raw listing metadata
  - `scored_listings`: For storing enriched and scored GPU listings
  - `quantized_listings`: For storing quantization capacities for GPU listings
- Implemented SQLAlchemy models in `glyphd/src/glyphd/sqlite/models.py`
- Set up Alembic for migrations in `glyphd/src/glyphd/sqlite/migrations/`
- Created a test harness in `glyphd/tests/test_schema.py`
- Documented the schema in `glyphd/src/glyphd/sqlite/SCHEMA.md`
- Added an `init-db` command to the CLI in `glyphd/src/glyphd/cli.py`

**Outcomes:**
- The schema is fully defined and can be instantiated via CLI or Python code
- All primary/foreign keys are defined where applicable
- The schema is extensible and can support new score fields
- Indexes are created on fields that are likely to be used in queries
- Migration scripts are included for future schema evolution
- The schema supports import versioning and timestamping of batches for differential updates

**Lessons learned:**
- The schema design needs to balance normalization with query performance
- Import versioning is crucial for tracking data provenance and enabling differential updates
- SQLAlchemy models provide a clean abstraction over the database schema

**Follow-up needed:**
- Implement the storage engine in TASK.persist.02.sqlite-engine-storage.md
- Implement the import endpoint in TASK.persist.03.api.import-listings-endpoint.md