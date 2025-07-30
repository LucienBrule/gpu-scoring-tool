

# TASK.audit.01.sqloader

## Title
Add SQL ResourceLoader and migrate `schema.sql` to structured resource context

## Status
Open

## Related
- [EPIC.audit.code-cleanup.md](../epics/open/EPIC.audit.code-cleanup.md)

## Rationale

The current `schema.sql` is loaded from a hardcoded file path in the local filesystem. This violates architectural boundaries and bypasses the ResourceLoader framework already in place for CSV and YAML formats.

Junie previously implemented a SQLite schema using `schema.sql`, but did not use the ResourceContext system. This task corrects that and makes SQL schemas first-class citizens in our resource architecture.

## Goal

Define and register a `SqlLoader` under the `BaseResourceContext` system. This will allow `.sql` files to be accessed consistently alongside YAML and CSV files. Once implemented, migrate the loading of `schema.sql` in glyphd to use `importlib.resources` via this loader.

## Requirements

- Implement `BaseSqlLoader` with a `.load_text()` method that returns SQL as a string
- Implement `GlyphdSqlLoader(BaseSqlLoader)` with `resource_uri = "glyphd.resources"`
- Register loader in `GlyphdResourceContext`
- Replace current open(path).read() with `GlyphdResourceContext().load_text("schema.sql")`
- Write a test to validate that `schema.sql` can be loaded via the loader
- Lint and test before handoff

## DX Loop

```bash
# From project root
uv run pytest glyphd/tests/test_schema.py
flake8 glyphd/src
```

## Acceptance Criteria

- No direct file path access for SQL remains in codebase ✅
- `schema.sql` loads via `ResourceContext` ✅
- Task is closed and summary is added to `EPIC.audit.code-cleanup.md` ✅

## ✅ Task Completed

**Changes made:**
- Created `BaseSqlLoader` class in `glyphsieve/src/glyphsieve/core/resources/base_sql_loader.py` with `load_text()` method
- Created `GlyphdSqlLoader` class in `glyphd/src/glyphd/core/resources/sql_loader.py` extending BaseSqlLoader
- Extended `ResourceContext` base class to support `load_text()` method for text-based resources
- Registered SQL loader in `GlyphdResourceContext` for `.sql` file extension
- Replaced direct `importlib.resources` usage in `sqlite_store.py` with `GlyphdResourceContext().load_text("sql/schema.sql")`
- Added `test_sql_loader()` test method to validate SQL loader functionality

**Outcomes:**
- SQL files are now first-class citizens in the ResourceContext system
- All direct file path access to `schema.sql` has been eliminated
- Schema loading now follows the same pattern as YAML and CSV resources
- All tests pass (8/8) and code is lint-clean (flake8 passes)

**Lessons learned:**
- The ResourceContext system needed extension to support text loading for non-Pydantic resources
- SQL files require different handling than structured data files (YAML/CSV) that map to Pydantic models
- The existing architecture was well-designed and easily extensible for new resource types

**Follow-up needed:**
- None - task is complete and all acceptance criteria met
