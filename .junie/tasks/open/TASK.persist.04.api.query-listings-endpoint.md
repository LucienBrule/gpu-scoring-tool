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