## Persona
You are the Timekeeper of the Market. Your role is to measure the change of value across time and expose signals of momentum, volatility, and opportunity.

## Title
Implement Core Delta Tracking for Price History Forecasting

## Purpose
When enriched and scored GPU listings are ingested, capture structured historical snapshots and compute deltas between successive snapshots for each listing. This enables price volatility analysis, trend detection, and forecasting.

## Requirements

1. **Snapshot Storage**
   - Define a SQLAlchemy model `ListingSnapshot` in `glyphd.models.sqlite` with fields:
     - `id: int` (primary key)
     - `model: str`
     - `price_usd: float`
     - `score: float`
     - `quantization_capacity: JSON` (match `QuantizationCapacitySpec`)
     - `seen_at: datetime`
     - `seller: str`
     - `region: str`
     - `source_url: str`
     - `heuristics: JSON`
   - On each ingestion via `/api/listings/import`, after persisting the listing, insert a new snapshot row.

2. **Delta Computation**
   - Implement `compute_delta(prev: ListingSnapshot, curr: ListingSnapshot) -> ListingDelta` in `glyphd.core.forecast`:
     - `price_delta: float = curr.price_usd - prev.price_usd`
     - `price_delta_pct: float = price_delta / prev.price_usd * 100`
     - `score_delta: float = curr.score - prev.score`
     - `timestamp: datetime` (now)
     - Include `model`, `region`, and `source_url` in the delta.
   - Define a SQLAlchemy model `ListingDelta` in `glyphd.models.sqlite`:
     - Fields for all delta properties plus foreign key to `ListingSnapshot.id`.

3. **Automated Delta Insertion**
   - Modify the ingestion endpoint implementation:
     - After snapshot insert, look up the most recent previous snapshot for the same `source_url`.
     - If found, compute the delta and persist a `ListingDelta`.

4. **Forecast API Endpoint**
   - Add GET `/api/forecast/deltas` in `glyphd.api.router`:
     - Query parameters: 
       - `model: Optional[str]`
       - `min_price_change_pct: Optional[float]`
       - `after: Optional[datetime]`
       - `region: Optional[str]`
     - Return JSON array of `ListingDelta` records sorted by `timestamp` descending.

## Constraints
- All storage and API logic must reside in `glyphd`.
- Use `ResourceContext` for any file-based configs; no direct filesystem access.
- Ensure referential integrity between `ListingSnapshot` and `ListingDelta`.
- Maintain stateless scoring; delta logic is part of the ingest pipeline, not the scoring engine.

## Tests
- **Unit tests** in `glyphd/tests/test_forecast.py`:
  - Verify `compute_delta` produces correct values for sample snapshots.
  - Validate no delta is created when only one snapshot exists.
- **Integration tests** in `glyphd/tests/test_api_forecast.py`:
  - With Docker Compose up, POST a CSV to `/api/listings/import` twice (with modified prices), then GET `/api/forecast/deltas` and assert one delta record.
- Tests must run against the live service; no mocking of endpoints.

## DX Runbook
```bash
# Build and start services
docker-compose up -d --build

# Ingest initial sample
curl -X POST http://localhost:8080/api/listings/import \
  -F "file=@sample/scored_sample_v1.csv"

# Simulate updated ingest
curl -X POST http://localhost:8080/api/listings/import \
  -F "file=@sample/scored_sample_v2.csv"

# Query deltas
curl "http://localhost:8080/api/forecast/deltas?model=RTX_A6000&min_price_change_pct=5"

# Run all tests and lint
pytest
uv run black glyphd/src
uv run isort glyphd/src
uv run ruff glyphd/src
uv run flake8 glyphd/src
```

## Completion Criteria
- Snapshots are recorded for each ingest event in the `listing_snapshots` table.
- Deltas are computed and stored in `forecast_deltas` (or `ListingDelta` table) upon each ingest.
- GET `/api/forecast/deltas` returns correct delta data filtered by query parameters.
- Unit and integration tests pass against the live Docker-composed service.
- All linting and formatting commands complete with zero errors.

## ✅ Task Completed

**Date Completed:** 2025-08-01

**Changes made:**
- ✅ **Database Models:** Created `ListingSnapshot` and `ListingDelta` SQLAlchemy models with proper relationships and foreign keys
- ✅ **Delta Computation Logic:** Implemented `compute_delta()` function in `glyphd.core.forecast` module with proper validation and error handling
- ✅ **Snapshot Creation:** Added `create_snapshot_from_listing()` helper function for converting listing data to snapshots
- ✅ **Ingestion Integration:** Modified `SqliteListingStore.insert_listings()` to automatically create snapshots and compute deltas during ingestion
- ✅ **API Endpoints:** Created `/api/forecast/deltas` endpoint with full query parameter support (model, min_price_change_pct, after, region, limit)
- ✅ **Additional Endpoint:** Added `/api/forecast/deltas/{delta_id}` for retrieving specific deltas with snapshot details
- ✅ **Unit Tests:** Comprehensive test suite in `glyphd/tests/test_forecast.py` covering all delta computation scenarios and edge cases
- ✅ **Integration Tests:** Full workflow tests in `glyphd/tests/test_api_forecast.py` testing ingestion → snapshot → delta → query pipeline
- ✅ **Code Quality:** All linting checks pass with zero errors

**Outcomes:**
- **Automated Snapshot Capture:** Every listing ingestion now automatically creates snapshots in `listing_snapshots` table
- **Delta Computation:** System automatically computes and stores price/score deltas between successive snapshots for the same source
- **Forecasting API:** Full REST API for querying historical deltas with comprehensive filtering capabilities
- **Price Volatility Analysis:** Enables tracking price changes over time with percentage calculations and trend detection
- **Production-Ready:** Complete error handling, validation, logging, and comprehensive test coverage

**Technical Achievements:**
- Proper SQLAlchemy relationships between snapshots and deltas
- Zero-division handling for price percentage calculations
- Validation to prevent cross-model and cross-source delta computation
- Efficient database queries with proper indexing and filtering
- RESTful API design with OpenAPI documentation
- Comprehensive test coverage for both unit and integration scenarios

**Key Features Delivered:**
- `POST /api/persist/listings` now creates snapshots and deltas automatically
- `GET /api/forecast/deltas` with filters: model, min_price_change_pct, after, region, limit
- `GET /api/forecast/deltas/{id}` for detailed delta information with snapshot context
- Complete price history tracking and volatility analysis capabilities
- Background-ready architecture for future enhancements

All completion criteria have been met and the system is ready for price forecasting and trend analysis.
