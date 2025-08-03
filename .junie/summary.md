# REST Ingestion API Epic & Task Refinement Summary

**Date:** 2025-08-01  
**Scope:** Planning and refinement pass for EPIC.ingest.rest-import-api and related tasks

## 🔍 What Was Changed

### Epic Enrichment
- **Added comprehensive current state analysis** showing existing functionality:
  - `/api/persist/listings` endpoint already handles JSON ingestion
  - Complete SQLite schema with `ImportBatch`, `ScoredListing`, etc.
  - `SqliteListingStore` with full CRUD operations
  - `GPUListingDTO` already includes `import_id` and `import_index` fields

- **Updated task list** to reflect actual task files vs. original epic description:
  - Aligned 5 existing tasks with their actual content
  - Identified 2 missing tasks that should be created
  - Clarified scope based on existing infrastructure

### Task File Refinement
Added **Planning Commentary** sections to all 5 task files:

1. **TASK.ingest.01.api.import-csv**: Clarified relationship to existing JSON endpoint
2. **TASK.ingest.02.api.import-from-pipeline-output**: Positioned as CSV-to-JSON bridge
3. **TASK.ingest.03.api.upload-and-validate-artifacts**: Framed as "dry-run" validation
4. **TASK.ingest.04.api.import-response-format**: Refocused on enhancing existing `ImportResultDTO`
5. **TASK.ingest.05.api.schema-versioning-support**: Added strategic context for API evolution

## 🤔 What Still Feels Unclear

### 1. **Raw vs. Scored Data Handling**
- Should CSV upload endpoints accept raw listings that need normalization/scoring?
- Or only accept already-processed data from the glyphsieve pipeline?
- The existing `/api/persist/listings` assumes scored data with `canonical_model`, `score`, etc.

### 2. **Pipeline Integration Strategy**
- How should the REST API integrate with the glyphsieve normalization pipeline?
- Should it trigger pipeline processing, or expect pre-processed input?
- Missing task: `TASK.ingest.07.api.pipeline-integration`

### 3. **Database Schema Gaps**
- `GPUListingDTO` has `import_index` field but `ScoredListing` table doesn't
- Should the database schema be updated to include `import_index`?
- How should raw vs. scored listings be differentiated in storage?

### 4. **Error Handling Scope**
- Current `ImportResultDTO` is success-focused (`record_count`, `first_model`, etc.)
- How should row-level validation errors be reported?
- Missing task: `TASK.ingest.06.api.error-handling-enhancement`

### 5. **File Storage Strategy**
- TASK.ingest.01 mentions saving to `import_batches/` folder
- But existing system uses direct database persistence
- Should uploaded files be stored on disk or just processed in-memory?

## ❓ Questions for the Operator

### Strategic Questions
1. **What's the primary use case?** 
   - Remote submission of raw CSV files that need processing?
   - API access to upload already-scored pipeline output?
   - Both scenarios with different endpoints?

2. **Pipeline Integration Approach:**
   - Should REST endpoints trigger glyphsieve pipeline processing?
   - Or should they only handle pre-processed data?
   - How should the API coordinate with CLI-based pipeline workflows?

### Technical Questions
3. **Database Schema Updates:**
   - Should `ScoredListing` table include `import_index` field?
   - How should we handle the raw vs. scored listing distinction?

4. **File Handling Strategy:**
   - Store uploaded files on disk for audit/replay?
   - Or process in-memory and discard after database insertion?

5. **Error Response Design:**
   - Extend `ImportResultDTO` with error fields?
   - Create separate error response models?
   - How granular should row-level error reporting be?

### Implementation Sequencing
6. **Task Priority:**
   - Should TASK.ingest.01 (CSV upload) be implemented first?
   - Or TASK.ingest.02 (pipeline output) since it's closer to existing functionality?

7. **Missing Tasks:**
   - Should we create the missing tasks before starting implementation?
   - Or implement existing tasks and create new ones as needed?

## 🎯 Recommended Next Steps

1. **Clarify strategic direction** on raw vs. scored data handling
2. **Define pipeline integration approach** before implementing endpoints
3. **Create missing tasks** for error handling and pipeline integration
4. **Update database schema** if `import_index` tracking is needed
5. **Start with TASK.ingest.02** (pipeline output) as it's closest to existing functionality

## 📊 Current Readiness Assessment

- **Epic:** Well-defined with clear architectural context ✅
- **Tasks 1-5:** Properly scoped with planning commentary ✅
- **Implementation readiness:** 🟡 Blocked on strategic decisions above
- **Technical foundation:** 🟢 Strong existing infrastructure to build upon