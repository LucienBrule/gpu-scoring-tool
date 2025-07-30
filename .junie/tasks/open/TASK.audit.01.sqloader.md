

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

- No direct file path access for SQL remains in codebase
- `schema.sql` loads via `ResourceContext`
- Task is closed and summary is added to `EPIC.audit.code-cleanup.md`
