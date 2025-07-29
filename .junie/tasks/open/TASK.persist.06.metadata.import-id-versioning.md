# TASK.persist.06.metadata.import-id-versioning

## Title
Implement Import Metadata: ID Tracking and Versioning for Listings

## EPIC Reference
[EPIC.persist.sqlite-store](../../epics/open/EPIC.persist.sqlite-store.md)

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