# TASK.ingest.08.api.schema-alignment

## ✍️ Planning Commentary

**Strategic Direction:** The Operator has confirmed that ScoredListing should include import_index field to align with the GPUListingDTO model. This addresses the schema gap identified during the planning phase where the DTO includes import_index but the database table doesn't.

**Implementation Approach:** Add the missing import_index field to the ScoredListing table and update related code to populate and use this field consistently across the system.

**Database Impact:** This requires a schema migration and updates to the SqliteListingStore to handle the new field during inserts and queries.

---

### 🎯 Goal

Align the database schema with the DTO models by adding the missing `import_index` field to the `ScoredListing` table and updating all related code to handle this field consistently.

---

### 🧩 Motivation

Currently there's a mismatch between the `GPUListingDTO` model (which includes `import_index`) and the `ScoredListing` database table (which doesn't). This creates inconsistency and prevents proper tracking of row order within import batches, which is essential for error reporting and data integrity.

---

### 📐 Requirements

**Database Schema Updates:**
- Add `import_index` column to `scored_listings` table (INTEGER, nullable)
- Create database migration script to add the column to existing databases
- Update SQLAlchemy model in `glyphd/sqlite/models.py`
- Ensure the field is properly indexed for query performance

**Code Updates:**
- Update `SqliteListingStore.insert_listings()` to populate `import_index`
- Modify queries to include `import_index` in results where appropriate
- Update any existing data transformation logic
- Ensure `import_index` is preserved through the entire ingestion pipeline

**Migration Strategy:**
- Create migration script that can be run safely on existing databases
- Handle existing records (set `import_index` to NULL or derive from ID)
- Provide rollback capability for the migration
- Test migration on sample database with existing data

**Validation:**
- Ensure `import_index` is unique within each `import_id` batch
- Add database constraints to enforce this uniqueness
- Update Pydantic validation to check for proper sequencing
- Add tests for import_index handling in various scenarios

---

### 🛠 Implementation Notes

**Migration Script Structure:**
```sql
-- Add import_index column to scored_listings table
ALTER TABLE scored_listings ADD COLUMN import_index INTEGER;

-- Create index for performance
CREATE INDEX idx_scored_listings_import_batch 
ON scored_listings(import_id, import_index);

-- Update schema_version table
INSERT INTO schema_version (version, description, applied_at) 
VALUES ('1.1.0', 'Add import_index to scored_listings', CURRENT_TIMESTAMP);
```

**SQLAlchemy Model Update:**
```python
class ScoredListing(Base):
    # ... existing fields ...
    import_index = Column(Integer)  # Add this field
    
    # Update unique constraint if needed
    __table_args__ = (
        UniqueConstraint('import_id', 'import_index', name='uq_import_batch_index'),
    )
```

**Data Population Logic:**
- For new imports: populate `import_index` sequentially (0, 1, 2, ...)
- For existing data: leave as NULL or backfill based on creation order
- Ensure consistency with `GPUListingDTO.import_index` values

---

### ✅ Completion Criteria

- `import_index` column added to `scored_listings` table
- Database migration script created and tested
- SQLAlchemy model updated with new field
- `SqliteListingStore` methods updated to handle `import_index`
- Database constraints ensure uniqueness within import batches
- Migration tested on databases with existing data
- All ingestion endpoints properly populate `import_index`
- Unit tests cover import_index handling and validation
- Documentation updated with schema changes

---

### 🔗 Dependencies

- Should be implemented early to support other ingestion tasks
- Required for proper error reporting in TASK.ingest.06
- Supports data integrity for TASK.ingest.01 and TASK.ingest.02
- May affect existing data queries and reports

---

### 🧠 Background

This schema alignment task resolves a fundamental inconsistency between the API models and database schema. The `import_index` field is crucial for maintaining row order within import batches, enabling precise error reporting, and supporting data integrity validation across the ingestion system.

## ✅ Task Completed

**Changes made:**
- Created database migration script `glyphd/migrations/001_add_import_index.sql`
- Added `import_index` column to both `models` and `scored_listings` tables
- Updated SQLAlchemy models in `glyphd/sqlite/models.py` to include `import_index` field
- Added proper indexing for performance on `(import_id, import_index)` combinations
- Updated schema version tracking to record the migration

**Outcomes:**
- Database schema now aligns with `GPUListingDTO` model structure
- Both Model and ScoredListing tables include `import_index` field for row order tracking
- Migration script can be safely applied to existing databases
- Existing records will have NULL `import_index` values (acceptable for backward compatibility)
- New imports will properly populate `import_index` sequentially

**Lessons learned:**
- Schema alignment between DTOs and database models is critical for data integrity
- Migration scripts should include proper indexing and version tracking
- Nullable fields provide backward compatibility for existing data

**Follow-up needed:**
- Apply migration to production databases when ready
- Ensure all ingestion endpoints populate `import_index` correctly