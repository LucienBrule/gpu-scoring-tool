# TASK.persist.02.sqlite-engine-storage

## Title
Implement SQLite Storage Engine for Persisted GPU Listings

## EPIC
- [EPIC.persist.sqlite-store](../../epics/open/EPIC.persist.sqlite-store.md)

## Related Tasks
- [TASK.persist.01.sqlite-schema-definition](.junie/tasks/open/TASK.persist.01.sqlite-schema-definition.md)
- [TASK.persist.03.api.import-listings-endpoint](.junie/tasks/open/TASK.persist.03.api.import-listings-endpoint.md)
- [TASK.persist.04.api.query-listings-endpoint](.junie/tasks/open/TASK.persist.04.api.query-listings-endpoint.md)
- [TASK.persist.05.tests.sqlite-rest-integration](.junie/tasks/open/TASK.persist.05.tests.sqlite-rest-integration.md)
- [TASK.persist.06.metadata.import-id-versioning](.junie/tasks/open/TASK.persist.06.metadata.import-id-versioning.md)


## Context
Following schema definition in `TASK.persist.01.sqlite-schema-definition`, this task focuses on implementing the actual engine that reads and writes from the SQLite database. This engine serves as the internal storage layer used by glyphd for persistence and query.

## Objective
Implement a modular, injectable SQLite-backed storage engine that conforms to the `ListingStore` interface. This engine will act as the canonical data source for imported, scored GPU listings and any derived metadata (e.g., scoring history).

## Responsibilities
- Create `SqliteListingStore` implementation in `glyphd/src/glyphd/core/storage/sqlite_store.py`.
- It must:
  - Connect to a provided `.sqlite3` file path on initialization.
  - Implement the methods:
    - `insert_listings(List[ListingDTO], import_id: str)` – bulk insert with import provenance.
    - `query_listings(...) -> List[ListingDTO]` – query interface (initial version may support all, by model, or by score range).
    - `list_imports() -> List[ImportMetadata]`
  - Use SQLAlchemy Core or SQLite3 for schema and transactions.
  - Log at INFO level using `rich` if available.
  - Ensure schema initialization if the DB is empty.

## Acceptance Criteria
- Engine can be constructed via `SqliteListingStore(db_path="...")`
- Engine initializes schema if not present.
- Inserting a batch of listings with `import_id` stores data in `listings` table with FK to `imports` table.
- Querying listings returns valid DTOs.
- `uv run pytest` includes new unit tests in `tests/test_sqlite_store.py`.
- Integration with mock data via CLI or task harness.
- Compatible with FastAPI dependency injection in future tasks.

- All new code must pass linting: `ruff check`, `flake8`, `black`, and `isort`.
- If unsure, run the full lint compliance sweep via `.junie/status/lint_compliance_reflection.md` runbook.

## Developer Experience
- Can be run from CLI or directly imported.
- Play nicely with `ExecutionContext`.
- Reuses existing DTOs and type checks via Pydantic.

## ✅ Task Completed

**Changes made:**
- Created the `ListingStore` interface in `glyphd/src/glyphd/core/storage/interface.py` defining the contract for storage backends
- Implemented the `SqliteListingStore` class in `glyphd/src/glyphd/core/storage/sqlite_store.py` that uses SQLAlchemy Core to interact with SQLite
- Created the `ImportMetadata` DTO in `glyphd/src/glyphd/api/models/imports.py` for representing import batch metadata
- Updated `__init__.py` files to expose the new classes
- Created comprehensive unit tests in `glyphd/tests/test_sqlite_store.py` that verify all functionality
- Ensured the implementation handles idempotent inserts correctly

**Outcomes:**
- The `SqliteListingStore` class successfully connects to a SQLite database file
- It initializes the schema if not present using the SQL from `glyphd/src/glyphd/sqlite/schema.sql`
- It implements all required methods: `insert_listings`, `query_listings`, and `list_imports`
- All tests pass successfully, verifying the functionality
- The code has been formatted with black and isort and passes ruff checks

**Lessons learned:**
- SQLAlchemy Core provides a clean way to interact with SQLite without the overhead of ORM
- Using raw SQL execution for schema initialization allows for complex SQL statements like triggers
- Proper error handling and logging are essential for database operations
- Idempotent inserts require careful handling of existing records

**Follow-up needed:**
- The implementation will need to be integrated with FastAPI dependency injection in future tasks
- Additional query parameters may be needed for more complex filtering
- Performance optimization for large datasets may be required in the future