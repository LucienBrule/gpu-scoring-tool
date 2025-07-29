# TASK.persist.05.tests.sqlite-rest-integration

## Title
Test SQLite-backed REST API Integration

## Status
Open

## EPIC
[EPIC.persist.sqlite-store.md](../../epics/open/EPIC.persist.sqlite-store.md)

## Objective

Implement a set of integration tests that validate the behavior of the SQLite-backed `glyphd` API endpoints, particularly those involved in importing and querying listings. These tests ensure that the REST API, the database layer, and the data lifecycle are functioning correctly together.

## Prerequisites

- Completion of:
  - [TASK.persist.01.sqlite-schema-definition.md](../open/TASK.persist.01.sqlite-schema-definition.md)
  - [TASK.persist.02.sqlite-engine-storage.md](../open/TASK.persist.02.sqlite-engine-storage.md)
  - [TASK.persist.03.api.import-listings-endpoint.md](../open/TASK.persist.03.api.import-listings-endpoint.md)
  - [TASK.persist.04.api.query-listings-endpoint.md](../open/TASK.persist.04.api.query-listings-endpoint.md)

## Scope

- Validate that listings can be imported via the API and persisted to SQLite ([TASK.persist.03.api.import-listings-endpoint.md](../open/TASK.persist.03.api.import-listings-endpoint.md), [TASK.persist.02.sqlite-engine-storage.md](../open/TASK.persist.02.sqlite-engine-storage.md))
- Confirm listings can be retrieved using the query endpoint with correct filters and pagination ([TASK.persist.04.api.query-listings-endpoint.md](../open/TASK.persist.04.api.query-listings-endpoint.md))
- Ensure metadata such as timestamps, import IDs, and canonical models are consistent and queryable ([TASK.persist.01.sqlite-schema-definition.md](../open/TASK.persist.01.sqlite-schema-definition.md))
- Run full-stack using the test client, not mocks

## Acceptance Criteria

- ✅ Pytest test file created under `glyphd/tests/test_persistence_api.py` ([TASK.persist.05.tests.sqlite-rest-integration.md](../open/TASK.persist.05.tests.sqlite-rest-integration.md))
- ✅ `TestClient` is used to perform full HTTP round-trip tests ([TASK.persist.05.tests.sqlite-rest-integration.md](../open/TASK.persist.05.tests.sqlite-rest-integration.md))
- ✅ At least one test covers:
  - POST to `/api/listings/import`
  - GET from `/api/listings`
  - Response structure validation
  - Presence of imported records ([TASK.persist.05.tests.sqlite-rest-integration.md](../open/TASK.persist.05.tests.sqlite-rest-integration.md))
- ✅ Database isolation between tests (use tmp path or fixtures) ([TASK.persist.05.tests.sqlite-rest-integration.md](../open/TASK.persist.05.tests.sqlite-rest-integration.md))
- ✅ Test passes locally and in CI ([TASK.persist.05.tests.sqlite-rest-integration.md](../open/TASK.persist.05.tests.sqlite-rest-integration.md))
- ✅ Test data includes at least two records with distinct canonical models and price fields ([TASK.persist.05.tests.sqlite-rest-integration.md](../open/TASK.persist.05.tests.sqlite-rest-integration.md))

## Developer Loop

- `uv run pytest glyphd/tests/test_persistence_api.py`
- `uv run glyphd` + `curl` or `httpie` for manual spot checks
- Inspect generated SQLite file under `.data/` or tempdir
- Confirm Swagger reflects correct OpenAPI behavior

## Related Tasks

- [TASK.persist.01.sqlite-schema-definition.md](../open/TASK.persist.01.sqlite-schema-definition.md)
- [TASK.persist.02.sqlite-engine-storage.md](../open/TASK.persist.02.sqlite-engine-storage.md)
- [TASK.persist.03.api.import-listings-endpoint.md](../open/TASK.persist.03.api.import-listings-endpoint.md)
- [TASK.persist.04.api.query-listings-endpoint.md](../open/TASK.persist.04.api.query-listings-endpoint.md)
- [TASK.persist.05.tests.sqlite-rest-integration.md](../open/TASK.persist.05.tests.sqlite-rest-integration.md)
- Linked to EPIC: [EPIC.persist.sqlite-store.md](../../epics/open/EPIC.persist.sqlite-store.md)

## Notes

This test validates the integration of multiple concerns: DTO modeling, loader logic, SQLite persistence, and REST exposure. Emphasis is on realistic flow coverage rather than exhaustiveness.

Tests should be clean, direct, and re-runnable without side effects.