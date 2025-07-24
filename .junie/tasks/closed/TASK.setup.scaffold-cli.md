

# TASK.setup.scaffold-cli.md

## 🧩 Task: Scaffold `glyphsieve` CLI Interface

Junie, your task is to scaffold the CLI entrypoint for the `glyphsieve` module using `click`. This is the foundational CLI that will drive the entire GPU pipeline workflow.

---

## 🎯 Goals

- Set up `glyphsieve` to be runnable as a CLI tool via:
  ```bash
  uv run glyphsieve
  ```

- Add a proper `__main__.py` that routes to `cli/main.py`
- Use `click` to create a CLI with the following subcommands:
  - `clean` (placeholder)
  - `normalize` (placeholder)
  - `score` (placeholder)

- Add a `--version` flag
- Use `rich` for CLI output formatting

---

## 📦 Dependencies to Add (with `uv add`, scoped to `glyphsieve/`)

```bash
uv add click pandas pydantic orjson python-dotenv
```

- ✅ `click` – command line interface
- ✅ `pandas` – CSV and tabular operations
- ✅ `pydantic` – DTOs and schema validation
- ✅ `orjson` – fast JSON parsing
- ✅ `python-dotenv` – env loading (future use)

---

## 🧱 Directory Structure (Post-Task Expected)

```
glyphsieve/
└── src/
    └── glyphsieve/
        ├── __main__.py         # entrypoint
        ├── cli/
        │   ├── __init__.py
        │   ├── main.py         # click CLI setup
        │   ├── clean.py        # placeholder module
        │   ├── normalize.py    # placeholder module
        │   └── score.py        # placeholder module
        ├── core/               # transformation logic
        └── utils/              # general helpers
```

---

## 📄 Notes

- Add proper `entry-points.console_scripts` to `pyproject.toml` (optional, for later installability)
- All CLI subcommands may be stubbed for now with simple `print()` statements
- Set up internal version tag (e.g. `glyphsieve.__version__`)

---

## ✅ Completion Criteria

- Running `uv run glyphsieve` yields CLI with help text and stubs
- `uv sync --all-packages` passes cleanly
- Subcommands stubbed and structured
- Pydantic is available and imported (even if unused yet)

Please close this task when complete and summarize anything notable at the end of this file.

---

## ✅ Task Completed

The `glyphsieve` CLI has been successfully scaffolded with the following components:

1. Added required dependencies:
   - click, pandas, pydantic, orjson, python-dotenv, rich

2. Created directory structure:
   - `__main__.py` entry point
   - `cli/` directory with subcommands
   - `core/` and `utils/` directories for future use

3. Implemented CLI with:
   - Main CLI group with version option
   - Three subcommands: `clean`, `normalize`, and `score`
   - Rich console formatting for output
   - Pydantic model in the `score` module

4. Updated package configuration:
   - Added version information to `__init__.py`
   - Updated entry points in `pyproject.toml`

All completion criteria have been met:
- Running `uv run glyphsieve` yields CLI with help text and stubs
- `uv sync --all-packages` passes cleanly
- Subcommands are stubbed and structured
- Pydantic is available and imported

The CLI is now ready for further development of the actual functionality in each subcommand.
