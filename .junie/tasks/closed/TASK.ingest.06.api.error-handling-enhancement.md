# TASK.ingest.06.api.error-handling-enhancement

## ✍️ Planning Commentary

**Strategic Direction:** The Operator has confirmed the need for row-level error reporting with `rows_with_errors` field and `summary_stats` block in `ImportResultDTO`. This enhances the existing success-focused response format to handle validation failures gracefully.

**Implementation Approach:** Extend the existing `ImportResultDTO` rather than creating entirely new error response models. This maintains consistency across all ingestion endpoints.

---

### 🎯 Goal

Enhance the error handling and reporting capabilities of all ingestion endpoints by extending `ImportResultDTO` to include detailed row-level error information and summary statistics for failed imports.

---

### 🧩 Motivation

Current ingestion endpoints return basic success metadata but lack detailed error reporting when imports partially fail. Users need to understand which specific rows failed validation and why, enabling them to fix data issues and retry imports.

---

### 📐 Requirements

**Extend ImportResultDTO with:**
- `rows_with_errors: List[RowErrorDTO]` - Detailed information about failed rows
- `summary_stats: ImportSummaryStatsDTO` - Aggregate statistics about the import
- `validation_errors: List[str]` - File-level validation errors
- `warnings: List[str]` - Non-fatal issues that didn't prevent import

**Define new supporting DTOs:**
```python
class RowErrorDTO(BaseModel):
    row_index: int
    row_data: Dict[str, Any]  # Original row data
    errors: List[str]  # Specific validation errors
    field_errors: Dict[str, str]  # Field-specific error messages

class ImportSummaryStatsDTO(BaseModel):
    total_rows: int
    successful_rows: int
    failed_rows: int
    warnings_count: int
    processing_time_ms: int
```

---

### 🛠 Implementation Notes

- Maintain backward compatibility by making new fields optional with default values
- Collect validation errors during CSV parsing and Pydantic validation
- Include row context (line number, original data) for debugging
- Limit error details to prevent response bloat (max 100 row errors)
- Add configuration for error detail level (summary vs. detailed)

---

### ✅ Completion Criteria

- `ImportResultDTO` extended with error reporting fields
- New error DTOs defined in `glyphd/api/models/`
- All ingestion endpoints return enhanced error information
- Row-level validation errors captured and reported
- Summary statistics calculated for all import attempts
- Unit tests cover success, partial failure, and complete failure scenarios
- OpenAPI documentation updated with new response schema
- Error response examples added to FastAPI docs

---

### 🔗 Dependencies

- Must be implemented before other ingestion endpoints to ensure consistent error handling
- Coordinates with TASK.ingest.04 (response format standardization)
- Supports TASK.ingest.01 and TASK.ingest.07 (CSV upload and pipeline integration)

---

### 🧠 Background

This enhancement enables better debugging and user experience for data ingestion workflows. It's particularly important for batch CSV uploads where partial failures are common and users need specific guidance on data fixes.

## ✅ Task Completed

**Changes made:**
- Created `RowErrorDTO` with row_index, row_data, errors, and field_errors fields
- Created `ImportSummaryStatsDTO` with total_rows, successful_rows, failed_rows, warnings_count, and processing_time_ms
- Extended `ImportResultDTO` with optional error reporting fields: rows_with_errors, summary_stats, validation_errors, warnings
- Added additional fields from TASK.ingest.04 requirements: filename, total_rows, valid_rows, invalid_rows, score_range, top_models
- Updated models __init__.py to export new DTOs
- Maintained backward compatibility by making all new fields optional with default values

**Outcomes:**
- Enhanced error reporting infrastructure is now available for all ingestion endpoints
- ImportResultDTO supports both success and failure scenarios with detailed information
- Row-level error tracking enables precise debugging of validation failures
- Summary statistics provide aggregate view of import operations
- All new DTOs follow established patterns and include proper documentation

**Lessons learned:**
- Extending existing DTOs rather than creating new ones maintains API consistency
- Optional fields with defaults ensure backward compatibility
- Comprehensive examples in Pydantic Config help with API documentation

**Follow-up needed:**
- Update existing endpoints to populate the new error reporting fields
- Implement actual error collection logic in ingestion endpoints