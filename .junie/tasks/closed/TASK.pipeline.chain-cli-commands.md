


# TASK.pipeline.chain-cli-commands.md

## 🧩 Task: Implement Chained Pipeline Runner

Junie, your task is to implement a `pipeline` subcommand in the `glyphsieve` CLI. This command should run the full canonical CLI chain: clean → normalize → enrich → score, using intermediate temp files or in-memory flow.

---

## 🎯 Objectives

- Add a `glyphsieve pipeline` CLI command
- Accept:
  - `--input` (raw CSV path)
  - `--output` (final scored CSV)
  - Optional: `--working-dir` to store intermediate outputs
  - Optional: `--dedup` to insert deduplication into the chain

- Execute the following CLI logic internally, in sequence:
  1. `clean`
  2. `normalize`
  3. `enrich`
  4. `score`

- Intermediate steps should write to temp files or working dir
- Final step should emit a CSV with all columns, ready for downstream use

---

## 📦 File Locations

- Command entry: `glyphsieve/cli/pipeline.py`
- You may reuse `main.py` to wire it into the root CLI

---

## 🧪 Output

- Final CSV contains:
  - Cleaned headers
  - Normalized model names
  - Enriched metadata
  - Score
- Optional: deduped listings if `--dedup` is enabled

---

## 🔧 Notes

- You may call into internal modules (e.g. `core.cleaning`, `core.normalization`, etc.) directly, or invoke subcommands programmatically
- Use temp file strategy or named stages: `stage_clean.csv`, `stage_normalized.csv`, etc.

🚫 You must not use `subprocess`, `os.system`, or shell invocations to run any step of the pipeline.
✅ Use internal Python functions and module imports directly (e.g. call `run_cleaning(...)` from `core.cleaning`)
This ensures the pipeline is testable, composable, and fully traceable within Python.

---

## 🧪 Tests

- Provide a test CSV
- Ensure full chain runs without error and output has expected structure

### 🧪 Additional Test Requirements

- Tests must be written using `pytest` and included under `glyphsieve/tests/`
- The test must validate:
  - End-to-end behavior of the pipeline function
  - That intermediate stages are invoked and chained properly
  - That output structure and row count are as expected

- You must **not** use `subprocess`, `os.system`, or CLI invocation within tests.
  - Use internal functions and API modules directly
  - Import from `glyphsieve.core.*` or `glyphsieve.cli.pipeline` as needed

This ensures all pipeline steps are testable as a service, not just a command.

---

## ✅ Completion Criteria

- `uv run glyphsieve pipeline --input scrape/foo.csv --output final.csv` works
- All intermediate stages executed
- Final file has full scored structure
- Optional: log timing or step durations

---

## ✍️ Context

This is the first step toward turning GlyphSieve into a long-lived daemon or streaming pipeline. Treat this as both utility and orchestration primer. Modular flow now, full service soon.
---

## ✅ Task Completed

Implemented the pipeline command that chains together the clean, normalize, enrich, and score steps, with an optional deduplication step. The command accepts input and output paths, as well as optional parameters for working directory, deduplication, models file, specs file, and weights file.

The implementation:
- Uses internal Python functions directly rather than subprocess or shell commands
- Handles intermediate files in a working directory or temporary directory
- Provides rich output with timing information for each step
- Includes comprehensive tests that verify the pipeline's functionality

All tests are passing, and the pipeline command is ready for use.
