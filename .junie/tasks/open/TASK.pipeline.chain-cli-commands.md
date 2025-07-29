## 🎯 Task: Add End-to-End Pipeline Execution to `glyphsieve` CLI

Junie, implement a new `pipeline` command in `glyphsieve.cli` that processes a raw GPU listing CSV through all core stages in sequence.

This single command must:
  - Clean the raw CSV
  - Normalize listings
  - Enrich with model metadata
  - Score each entry
  - Generate an insight report

---

## 🧪 Requirements

- Add a `@app.command("pipeline")` to `glyphsieve.cli`
- Command flags:
  - `--input <path>`: existing raw CSV (must exist and be readable)
  - `--output <path>`: scored CSV destination (parent directory must be writable)
  - `--report <path>` (optional): insight report (Markdown or HTML)
  - `--debug`: emit intermediate outputs for inspection
- Validation:
  - Fail fast with a clear error if `--input` is missing or invalid
  - Create `--output` parent directory if needed
- In-memory chaining:
  - Invoke internal `clean()`, `normalize()`, `enrich()`, `score()`, and `report()` functions
  - Avoid spawning subprocesses or performing external CLI calls
- Debug behavior:
  - When `--debug` is set, write intermediate files alongside `--output`:
    1. `01.cleaned.csv`
    2. `02.normalized.csv`
    3. `03.scored.csv`
- Final output:
  - Print a summary line on success, e.g.  
    `✅ Pipeline complete: scored CSV → output.csv`

---

## 🔄 Example

```bash
uv run glyphsieve pipeline \
  --input scrape/NVIDIA_A2/a2_raw.csv \
  --output analysis/a2_scored.csv \
  --report analysis/a2_report.md \
  --debug
```

---

## 🔍 Additional Notes

- Use the existing CLI modules; do **not** duplicate logic.
- Follow project linting rules: run `ruff`, `flake8`, `isort`, and `black` with zero errors or diffs.
- Ensure `--help` output is clear and documents all flags.
- Handle errors gracefully with user-friendly messages.

---

## ✅ Completion Criteria

- `glyphsieve pipeline` command is available with all flags and help text
- Pipeline runs end-to-end successfully on a real CSV, producing valid scored output
- Intermediate files appear correctly when `--debug` is used
- Input and output path validations work as specified
- A success summary line is printed at the end
- Unit and CLI tests cover:
  - Normal flow (all flags, no flags)
  - Error flow (missing input, invalid CSV)
  - Debug flow (intermediate files)
- All tests pass under `uv run pytest`
- Codebase passes `ruff`, `flake8`, `isort`, and `black`