# Junie Guidelines (v0.1.0)

Welcome to Junie, the assistant task and tooling layer for `gpu-scoring-tool` and `glyphsieve`. This document outlines best practices, project norms, execution patterns, and guidance for maintaining and contributing to this evolving research system.

---

## 🧠 Project Overview

Junie supports the broader purpose of this repository: analyzing and interpreting real-world GPU market dynamics. She helps scaffold, extend, and maintain structured data pipelines and normalization tools across a multi-layered system.

---

## 📁 Repo Structure (High-Level)

- `glyphsieve/` — Python 3.12 project managed via `uv`; home of core normalization and scoring code.
- `sieveviz/` — Visualization layer (JS/HTML/CSS). Junie does not modify this without explicit instruction.
- `scrape/` — Raw CSV data scraped from sellers (organized by SKU).
- `recon/` — OSINT-style manual collection folders; Junie reads, but does not modify.
- `.junie/` — Junie's own memory and operational space.

---

## ⚙️ Tooling & Runtime

- This project uses [`uv`](https://github.com/astral-sh/uv) for Python environment and dependency management.
    - Add packages from within the relevant subproject:
      ```bash
      uv add <package>
      ```
    - Sync all environments:
      ```bash
      uv sync --all-packages
      ```
    - If the environment becomes stale (e.g. due to renames), reset with:
      ```bash
      rm uv.lock && uv sync --all-packages
      ```

### Scripting and Development Patterns

- Python 3.12 is the standard runtime for all `glyphsieve/` code
- Typer-based CLI tooling is planned for command-line interfaces
- When creating new scripts, follow these conventions:
  - Include docstrings with purpose and usage examples
  - Add type hints to function signatures
  - Implement proper error handling and logging
  - Create unit tests for core functionality

### Language Interoperability

- Kotlin/TypeScript interop for DTO definitions and structured pipelines is planned
- When working with cross-language data structures:
  - Document schema definitions in both languages
  - Ensure consistent naming conventions across language boundaries
  - Validate data integrity during language transitions

---

## ✅ Best Practices

- Do not modify `sieveviz/` unless assigned
- Always validate your output schemas — column alignment matters
- Output artifacts (e.g. normalized CSVs, enriched JSONs) should be written to a defined stage or subfolder
- Respect source-of-truth hierarchy: normalized data overrides raw scraped listings

### Pipeline Boundaries

- Junie operates primarily on the `glyphsieve/` codebase and data processing pipelines
- Junie does not modify raw data in `scrape/` but can read and process it
- Junie does not modify `recon/` directory contents but can analyze and extract insights
- Junie can suggest visualization improvements but should not directly modify `sieveviz/` without explicit instruction

### Schema Evolution Tracking

- Document all schema changes in comments at the top of affected files
- When modifying data structures, include version numbers (e.g., `v1.0 -> v1.1`)
- Maintain backward compatibility where possible
- Create migration scripts when breaking changes are necessary

### Clean File Output Discipline

- All generated files should include creation timestamp and source information
- Use consistent naming patterns for output files (e.g., `<model>_<process>_<date>.csv`)
- Include headers in all CSV outputs
- Validate column alignment and data types before writing files
- Prefer structured directories over flat file organization
- Do not pollute the repo root with temporary output files; use a dedicated directory (e.g., `tmp/output/`) for testing CLI commands

---

## 📓 Task System

Junie follows a custom task format located at `.junie/tasks/`, inspired by broader system agent conventions.

### Task Naming Convention:

```
tasks/{open,closed}/TASK.<category>.<title>.md
```

- Use meaningful `category` and `title` slugs
- Each task should be scoped and clear in purpose

### Task Lifecycle:

- Junie should only close a task when the delivery criteria are met
- Junie **must automatically** close tasks upon completion without being explicitly instructed to do so
- To close a task, move the task file from `.junie/tasks/open/` to `.junie/tasks/closed/`
- If a task is explored but not completed, **do not close it**
- Upon closure, Junie **must** append a short summary or comment block describing what was done, learned, or blocked

---

## 🛣️ Forward Guidance

- Keep `.junie/guidelines.md` current as norms evolve
- Ask clarifying questions via task comments or supplemental markdown blocks
- Assume that everything here is part of a live, breathing architecture — clean inputs and structured communication enable robust cognition across all tools

Junie is expected to operate with care, precision, and clarity. Welcome to the forge.
