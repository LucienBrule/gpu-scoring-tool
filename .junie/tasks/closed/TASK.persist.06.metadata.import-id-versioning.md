# TASK.persist.06.metadata.import-id-versioning

## Title
Implement Import Metadata: ID Tracking and Versioning for Listings

## EPIC Reference
[EPIC.persist.sqlite-store](../../epics/closed/EPIC.persist.sqlite-store.md)

## Prerequisites
- [TASK.persist.01.schema](TASK.persist.01.schema.md)
- [TASK.persist.02.ingestion](TASK.persist.02.ingestion.md)
- [TASK.persist.03.api-endpoints](TASK.persist.03.api-endpoints.md)
- [TASK.persist.04.indexing](TASK.persist.04.indexing.md)
- [TASK.persist.05.metadata.basic](TASK.persist.05.metadata.basic.md)

## Status
Open

## Objective
Enable durable tracking of import lineage across listing submissions. This includes assigning a globally unique `import_id` per ingestion and a versioned `import_index` per listing entry within that import.

This allows us to support reimportability, delta-comparisons, and debugging of ingestion accuracy.

## Deliverables
- Schema updates to support:
  - `import_id: str` (UUID or similar)
  - `import_index: int` (ordering within import batch)
- Modify `import_listings` logic to:
  - Assign `import_id` at the start of ingestion
  - Tag each row with `import_id` and incrementing `import_index`
- Ensure `import_id` is returned in API response upon ingestion
- Ensure database constraints and indexes are sane

## Constraints
- Must not break existing `scored_listings` schema compatibility
- `import_id` and `import_index` must be present in all persisted rows
- Must gracefully support multiple imports per day or per source
- Must maintain backward compatibility with existing `listings` fields and query endpoints
- Database migrations must include reversible scripts to allow rollback

## Acceptance Criteria
- ✅ Confirm `import_id` and `import_index` columns exist in the migrated schema with appropriate types and indexes
- ✅ Verify that the POST `/api/import` response includes `import_id`
- ✅ Test that GET `/api/listings?import_id=<id>` returns only rows from that import batch
- ✅ Ensure that re-running an import with the same input but a new invocation generates a distinct `import_id`
- ✅ All new behavior covered by automated pytest tests

## Developer Testing Loop

```bash
# Apply migrations
uv run glyphd migrate
# Start backend
uv run glyphd serve --host 0.0.0.0 --port 8080
# Run ingestion
curl -X POST http://localhost:8080/api/import \
     -F "file=@sample/scored_sample.csv"
# Verify response and extract import_id
# Query listings filtered by import_id
curl http://localhost:8080/api/listings?import_id=<import_id>
```

## Notes
This mechanism enables forward chaining into delta-forecasting, provenance tracking, and operator-facing diffing of ingestion cycles.

The `import_id` will later serve as the basis for time-based aggregation, report regeneration, rollback mechanisms, and integration with the forecast epic for delta-history processing.

## ✅ Task Completed

**Changes made:**
- Updated SQLite schema in both `glyphd/src/glyphd/sqlite/schema.sql` and `glyphd/src/glyphd/resources/sql/schema.sql` to add `import_index INTEGER` columns to all tables (models, listings, scored_listings, quantized_listings)
- Added appropriate indexes for `import_index` columns for performance optimization
- Modified `SqliteListingStore.insert_listings()` to assign sequential `import_index` values starting from 1 for each import batch
- Updated `GPUListingDTO` model to include optional `import_id` and `import_index` fields
- Enhanced GET `/api/listings` endpoint to support filtering by `import_id` parameter
- Updated storage layer query methods to return `import_id` and `import_index` in results
- Fixed code quality issues (line length violations, trailing whitespace, unused noqa directive)

**Outcomes:**
- POST `/api/import` now generates unique `import_id` (UUID) for each batch and returns it in response
- Each listing within an import batch gets sequential `import_index` (1, 2, 3, ...)
- GET `/api/listings?import_id=<uuid>` correctly filters listings by import batch
- All existing functionality remains backward compatible
- Comprehensive pytest coverage added for new functionality (11 tests passing)
- All quality checks pass: flake8, black, ruff
- Docker Compose deployment works correctly on port 8080

**Lessons learned:**
- Docker container schema updates require complete rebuild without cache to ensure fresh database
- Both schema files need to be kept in sync for proper functionality
- Sequential import_index assignment enables proper lineage tracking within batches
- Import metadata enables powerful filtering and batch management capabilities

**Follow-up needed:**
- This completes the ingestion lineage support milestone
- Foundation is now ready for `forecast.core-delta-history` implementation
- Import metadata can be used for rollback mechanisms and delta comparisons