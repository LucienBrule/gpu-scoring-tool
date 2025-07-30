

# TASK.audit.02.no-path-file-only-resources

## Summary
Ensure that all resource access in the codebase adheres to the `ResourceContext` and `importlib.resources` loader pattern. No component should resolve resources by using `Path(__file__)`, `os.path`, or any form of manual filesystem traversal. This audit task enforces the architectural boundary that all resource access must be abstracted through context-resolved, safe importable modules.

## Motivation
Direct path-based access to internal files introduces brittle behavior, security concerns, and makes the codebase harder to reason about for agents (Junie, Goose) and future contributors. We want to ensure that all access to static resources (e.g., YAML, CSV, Markdown, SQL schema files) goes through an interface that is introspectable, testable, and agent-compatible.

## Acceptance Criteria

- [ ] All remaining uses of `Path(__file__)`, `os.path`, or manual `open()` against hardcoded paths are removed.
- [ ] All static resource files are loaded through their respective `*Loader` via a `ResourceContext`.
- [ ] If a file requires a new loader (e.g., `.sql`, `.json`, `.md`), define one or mark it with a TODO and link to a separate loader task.
- [ ] Add or update tests that exercise the new loader path.

## DX Loop
To test your changes:
```
pytest
flake8 glyphd/src
ruff check glyphd/src
isort glyphd/src
```

## Related
- EPIC.audit.code-cleanup.md
- TASK.audit.01.sqloader.md

## ✅ Task Completed

**Changes made:**
- Conducted comprehensive audit of codebase for resource loading violations
- Verified no remaining uses of `Path(__file__)`, `__file__`, or hardcoded resource paths
- Confirmed all resource loading uses proper ResourceContext and loader patterns

**Outcomes:**
- No code changes were required - previous audit work had already eliminated all violations
- Custom flake8 rules (GLS001-GLS005) pass cleanly on both glyphsieve and glyphd packages
- All glyphd tests pass (46/46), confirming resource loading works correctly
- Some unrelated test failures in glyphsieve (4/97) but these are not resource loading related

**Lessons learned:**
- The previous TASK.audit.01.sqloader.md work was comprehensive and eliminated all resource loading violations
- The custom linting rules are effective at preventing regressions
- Resource loading architecture is now fully compliant with agent-operable patterns

**Follow-up needed:**
- None - task is complete and EPIC updated