# GPU Scoring Tool API Design Summary

**Version:** 0.1.0  
**Last Updated:** 2025-08-01  
**API Base URL:** `/api`

## Overview

The GPU Scoring Tool API (Glyphd) is a comprehensive REST API service that provides GPU market data ingestion, processing, and analysis capabilities. The API is built with FastAPI and follows modern REST principles with comprehensive error handling, schema versioning, and extensive validation.

## Architectural Principles

### 1. **Dual-Path Ingestion Strategy**

The API implements a sophisticated dual-path ingestion system to handle different data sources and processing requirements:

- **Raw Data Path:** Accepts unprocessed CSV files and automatically processes them through the glyphsieve normalization and scoring pipeline
- **Pre-Processed Data Path:** Accepts already-scored CSV files from pipeline outputs for direct database insertion

This design enables both automated data processing workflows and direct integration with external scoring systems.

### 2. **Schema-First Design**

All API endpoints use strongly-typed Pydantic models with comprehensive validation:
- Request/response models are defined as DTOs (Data Transfer Objects)
- Automatic OpenAPI schema generation
- Built-in validation with detailed error messages
- Type safety across the entire API surface

### 3. **Comprehensive Error Handling**

The API implements multi-level error reporting:
- **HTTP Status Codes:** Proper use of 4xx for client errors, 5xx for server errors
- **Row-Level Errors:** Detailed validation errors for individual data rows
- **Summary Statistics:** Aggregate error reporting for batch operations
- **Validation Warnings:** Non-fatal issues that don't prevent processing

### 4. **Schema Versioning & Backward Compatibility**

Built-in versioning system ensures API evolution without breaking existing clients:
- Enum-based version management (`v1.0`, `v1.1`)
- Version introspection endpoints
- Backward-compatible field additions using optional fields
- Client guidance for unsupported versions

## API Endpoint Catalog

### Data Ingestion Endpoints

#### `POST /api/import/csv`
**Purpose:** Raw CSV file upload with automatic pipeline processing  
**Design Rationale:** Enables end-to-end processing of unstructured GPU listing data

**Key Design Choices:**
- Multipart form-data upload for file handling
- File size validation (50MB limit)
- UTF-8 encoding enforcement
- Synchronous processing with background capability planned
- Integration with glyphsieve pipeline (normalize → enrich → score)

**Request Format:**
```http
POST /api/import/csv
Content-Type: multipart/form-data

file: [CSV file with title, price, condition, seller columns]
```

**Response:** `ImportResultDTO` with processing statistics

#### `POST /api/imports/from-pipeline`
**Purpose:** Import pre-processed CSV from glyphsieve pipeline output  
**Design Rationale:** Direct integration with existing pipeline workflows

**Key Design Choices:**
- JSON request body with file path reference
- Expects fully-scored data with specific schema
- Direct conversion to `GPUListingDTO` objects
- No additional processing required

**Request Format:**
```json
{
  "input_csv_path": "tmp/wamatek_final.csv",
  "source_label": "Wamatek July 2025",
  "campaign_id": "wamatek-q3-2025",
  "metadata": {"region": "US", "vendor": "wamatek"}
}
```

#### `POST /api/persist/listings`
**Purpose:** Direct JSON array ingestion for programmatic access  
**Design Rationale:** Enables direct API integration without file handling

**Key Design Choices:**
- Accepts array of `GPUListingDTO` objects
- Immediate database persistence
- Automatic snapshot creation for forecasting
- Batch processing with transaction safety

### Validation & Quality Assurance

#### `POST /api/ingest/upload-artifact`
**Purpose:** File validation without persistence ("dry-run" validation)  
**Design Rationale:** Enables pre-flight validation and debugging

**Key Design Choices:**
- Multi-format support (CSV, JSON, YAML)
- Optional disk saving for debugging (`save_to_disk` parameter)
- Automatic schema detection and validation
- Detailed validation reporting without side effects

**Response:** `ArtifactValidationResultDTO` with validation results

### Forecasting & Analytics

#### `GET /api/forecast/deltas`
**Purpose:** Query price volatility and trend analysis  
**Design Rationale:** Enable market intelligence and forecasting capabilities

**Key Design Choices:**
- Comprehensive query parameter filtering:
  - `model`: Filter by GPU model name
  - `min_price_change_pct`: Minimum price change threshold
  - `after`: Timestamp-based filtering
  - `region`: Geographic filtering
  - `limit`: Result pagination (max 1000)
- Absolute percentage change filtering (handles both positive and negative changes)
- Descending timestamp ordering for recent-first results

#### `GET /api/forecast/deltas/{delta_id}`
**Purpose:** Detailed delta information with snapshot context  
**Design Rationale:** Enable deep-dive analysis of specific price changes

**Key Design Choices:**
- Resource-based URL pattern
- Includes related snapshot data
- Proper 404 handling for missing resources

### Schema Management

#### `GET /api/schema/versions`
**Purpose:** API version discovery and compatibility checking  
**Design Rationale:** Enable client version negotiation and compatibility

**Key Design Choices:**
- Returns supported versions, default version, and current version
- Enables client-side compatibility checking
- Supports API evolution planning

#### `GET /api/schema/versions/{version}`
**Purpose:** Specific version support validation  
**Design Rationale:** Enable precise version compatibility checking

## Data Models & Response Formats

### ImportResultDTO
**Purpose:** Standardized response format for all ingestion operations

**Design Philosophy:**
- **Backward Compatibility:** New fields are optional with sensible defaults
- **Rich Metadata:** Comprehensive information for monitoring and debugging
- **Error Transparency:** Detailed error reporting without information loss
- **Schema Versioning:** Built-in version tracking for API evolution

**Key Fields:**
```json
{
  "import_id": "UUID",
  "record_count": "int",
  "first_model": "string",
  "last_model": "string", 
  "timestamp": "datetime",
  "filename": "string (optional)",
  "total_rows": "int (optional)",
  "valid_rows": "int (optional)",
  "invalid_rows": "int (optional)",
  "score_range": "[float, float] (optional)",
  "top_models": "string[] (optional)",
  "rows_with_errors": "RowErrorDTO[] (optional)",
  "summary_stats": "ImportSummaryStatsDTO (optional)",
  "validation_errors": "string[] (optional)",
  "warnings": "string[] (optional)",
  "schema_version": "SchemaVersion"
}
```

### Error Handling Models

#### RowErrorDTO
**Purpose:** Detailed row-level error reporting

**Design Rationale:**
- Enables precise debugging of data quality issues
- Includes original data context for error resolution
- Separates general errors from field-specific errors

#### ImportSummaryStatsDTO
**Purpose:** Aggregate statistics for batch operations

**Design Rationale:**
- Provides high-level operation overview
- Includes performance metrics (processing time)
- Enables monitoring and alerting

## Design Patterns & Best Practices

### 1. **Dependency Injection**
- FastAPI's dependency injection system for database connections
- Testable and modular architecture
- Clean separation of concerns

### 2. **Resource-Based URLs**
- RESTful resource naming conventions
- Consistent URL patterns across endpoints
- Proper HTTP method usage

### 3. **Comprehensive Logging**
- Structured logging with context information
- Performance and error tracking
- Audit trail for all operations

### 4. **Validation Strategy**
- Multi-layer validation (HTTP, Pydantic, business logic)
- Early validation with detailed error messages
- Graceful handling of malformed data

### 5. **Transaction Safety**
- Database transactions for batch operations
- Rollback capability for failed operations
- Idempotent operations where possible

## Integration Patterns

### Pipeline Integration
The API seamlessly integrates with the glyphsieve processing pipeline:

1. **Raw CSV Upload** → **Normalization** → **Enrichment** → **Scoring** → **Database Persistence**
2. **Automatic Snapshot Creation** → **Delta Computation** → **Forecasting Data**

### Error Recovery
- Partial success handling for batch operations
- Detailed error reporting for failed rows
- Continuation capability for recoverable errors

### Monitoring & Observability
- Comprehensive logging at all levels
- Performance metrics collection
- Error rate tracking and alerting

## Security Considerations

### Input Validation
- File size limits (50MB for uploads)
- File type validation (extension and content)
- Encoding validation (UTF-8 enforcement)
- SQL injection prevention through parameterized queries

### Error Information Disclosure
- Sanitized error messages in production
- Detailed errors available in development mode
- No sensitive information in error responses

## Performance Characteristics

### File Processing
- Streaming CSV processing for large files
- Memory-efficient pipeline processing
- Configurable batch sizes for database operations

### Query Optimization
- Indexed database queries for forecasting endpoints
- Pagination support for large result sets
- Query parameter validation and limits

### Scalability Considerations
- Background processing capability (planned)
- Stateless API design for horizontal scaling
- Database connection pooling

## Future Extensibility

### Planned Enhancements
- Background job processing for large files
- WebSocket support for real-time updates
- Additional file format support
- Enhanced forecasting algorithms

### API Evolution Strategy
- Schema versioning for backward compatibility
- Feature flags for gradual rollouts
- Deprecation warnings for obsolete endpoints

## OpenAPI Documentation

The API provides comprehensive OpenAPI documentation available at:
- **Swagger UI:** `/docs`
- **ReDoc:** `/redoc`
- **OpenAPI Schema:** `/openapi.json`

### Documentation Features
- Interactive API exploration
- Request/response examples
- Schema validation documentation
- Error response documentation

## Conclusion

The GPU Scoring Tool API represents a mature, production-ready REST API with comprehensive data ingestion, validation, and analysis capabilities. The design emphasizes reliability, extensibility, and developer experience while maintaining high performance and data integrity standards.

The dual-path ingestion strategy, comprehensive error handling, and built-in forecasting capabilities make it suitable for both automated data processing workflows and interactive analysis applications.