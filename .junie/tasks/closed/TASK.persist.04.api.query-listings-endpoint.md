# TASK.persist.04.api.query-listings-endpoint

## Status
Open

## Epic
EPIC.persist.sqlite-store

## Links
- [EPIC.persist.sqlite-store](../epics/open/EPIC.persist.sqlite-store.md)
- [TASK.persist.03.api.import-listings-endpoint](TASK.persist.03.api.import-listings-endpoint.md)
- [TASK.persist.05.tests.sqlite-rest-integration](TASK.persist.05.tests.sqlite-rest-integration.md)

## Objective
Implement a FastAPI route that allows querying stored GPU listings from the SQLite database. This endpoint will power the data retrieval layer for the frontend and future report views.

## Motivation
Once listings are stored via the import endpoint, we need a reliable, structured way to retrieve them. This API should support pagination and optional filters for key fields like model, condition, and price range.

## Implementation Requirements
- Define a GET `/api/listings` route in `glyphd/src/glyphd/api/routes/listings.py`.
- Import and use the Pydantic model `ListingDTO` from `glyphd.api.models.listings`.
- Inject a database session or repository via `glyphd.core.dependencies.get_listing_repository`.
- Use SQLAlchemy to query the listings table, e.g., `session.query(Listing).filter(...)`.
- Use the existing fuzzy-matching utility from `glyphsieve` (e.g., import and use `fuzzy_match` from `glyphsieve.core.heuristics`) to apply fuzzy matching on the `model` field.
- Support query parameters:
  - `model` (optional, fuzzy match on canonical model name)
  - `min_price`, `max_price` (optional float filters)
  - `limit` (default 100, max 1000), `offset` for pagination
- Return a paginated list of listings in JSON format using `ListingDTO` or equivalent Pydantic response model.

## Acceptance Criteria
- Route returns correct filtered results when listings exist.
- Pagination works correctly with large datasets.
- Returns `200 OK` with results or `[]` when no listings match.
- Returns `400 Bad Request` for invalid query parameters.
- Example cURL:
  ```
  curl GET http://localhost:8000/api/listings?model=H100_PCIE_80GB&min_price=1000&limit=50
  ```
- Covered by integration tests in `TASK.persist.05.tests.sqlite-rest-integration`.

## ✅ Task Completed

**Changes made:**
- Created `glyphd/src/glyphd/core/dependencies/listing_repository.py` with `get_listing_repository()` dependency function
- Extended `ListingStore` interface in `glyphd/src/glyphd/core/storage/interface.py` to support new parameters: `min_price`, `max_price`, `limit`, `offset`
- Updated `SqliteListingStore.query_listings()` method in `glyphd/src/glyphd/core/storage/sqlite_store.py` to:
  - Support price-based filtering with `min_price` and `max_price` parameters
  - Implement fuzzy matching for model field using `glyphsieve.core.normalization.fuzzy_match`
  - Add pagination support with `limit` and `offset` parameters
  - Maintain backward compatibility with existing parameters
- Implemented GET `/api/listings` endpoint in `glyphd/src/glyphd/api/routes/listings.py` with:
  - Query parameter validation (min_price >= 0, max_price >= 0, limit 1-1000, offset >= 0)
  - Price range validation (min_price <= max_price)
  - Proper error handling with 400/500 HTTP status codes
  - Fuzzy matching support for model names
  - Pagination with default limit of 100, max 1000
- Moved existing endpoint to `/listings/legacy` to preserve backward compatibility

**Outcomes:**
- GET `/api/listings` endpoint successfully implemented and accessible
- All unit tests pass (30 passed, 46 warnings)
- Code passes all linting checks (ruff, black, isort)
- Docker Compose builds and runs successfully
- Endpoint supports all required query parameters: `model`, `min_price`, `max_price`, `limit`, `offset`
- Fuzzy matching works for model field with 70% threshold
- Returns appropriate HTTP status codes: 200 for success, 400 for invalid params, 500 for server errors
- Returns empty array `[]` when no matches found

**Lessons learned:**
- The fuzzy_match function from glyphsieve requires a specific dictionary format for models
- SQLAlchemy Core queries need careful parameter binding for dynamic IN clauses
- FastAPI Query parameter validation provides built-in range checking (ge, le)
- Maintaining backward compatibility while adding new functionality requires careful endpoint design

**Follow-up needed:**
- Integration tests in TASK.persist.05.tests.sqlite-rest-integration should cover this endpoint
- Consider adding more sophisticated fuzzy matching options (configurable threshold)
- Monitor performance with large datasets and consider adding database indexes if needed