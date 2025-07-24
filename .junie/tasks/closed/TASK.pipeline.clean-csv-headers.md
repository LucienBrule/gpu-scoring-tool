# TASK.pipeline.clean-csv-headers.md

## 🧩 Task: Implement CSV Header Cleaning Pipeline

Junie, your task is to implement a `clean` subcommand under the `glyphsieve` CLI. This command should clean CSV headers and output a normalized file for downstream processing.

---

## 🎯 Objectives

- Implement `glyphsieve clean` as a `click` subcommand
- Accept the following arguments:
  - `--input` (path to CSV file)
  - `--output` (optional; if not set, default to `cleaned_<filename>.csv`)
  - `--dry-run` (optional; if set, do not write file — just print detected header transformation)

- Perform the following header transformations:
  - Trim whitespace
  - Convert to lowercase
  - Replace spaces with underscores
  - Standardize names such as:
    - `"Title"` → `title`
    - `"Price (USD)"` → `price_usd`
    - `"Model Name"` → `model`

- Write the cleaned CSV to the specified output path (unless `--dry-run` is used)

---

## 📦 Location

- CLI logic lives in: `glyphsieve/src/glyphsieve/cli/clean.py`
- Cleaning function lives in: `glyphsieve/src/glyphsieve/core/cleaning.py`
- Helpers may live in: `glyphsieve/src/glyphsieve/utils/`

---

## 🧪 Testing

- Create a `tests/` directory inside the `glyphsieve/` project
- Write test(s) using `pytest` to validate the cleaning logic
- Use **synthetic CSV input** via `StringIO` or test fixture files

---

## ✅ Completion Criteria

- `uv run glyphsieve clean --input foo.csv --output bar.csv` works as expected
- `--dry-run` prints a mapping like:
  ```
  Detected columns:
    "Title" → "title"
    "Price (USD)" → "price_usd"
    ...
  ```
- Test coverage is present and can be run with:
```bash
uv add --dev pytest && uv run pytest
```

---

## ✍️ Notes

This is your first actual pipeline operation and establishes trust in CSV input handling. You may stub placeholder columns (e.g. `model`, `condition`) in future passes. The primary goal is to validate that all scraped input files can be passed through `clean` before normalization.

Close this task when complete. If relevant, append a summary or follow-up notes here.

## ✅ Completion Notes (July 24, 2023)

The CSV header cleaning pipeline has been successfully implemented with the following features:

1. Implemented `glyphsieve clean` as a CLI command with the required options:
   - `--input` (required): Path to CSV file to clean
   - `--output` (optional): Path for cleaned output CSV file
   - `--dry-run` (optional): Print detected header transformation without writing file

2. Implemented header transformations:
   - Trimming whitespace
   - Converting to lowercase
   - Replacing spaces with underscores
   - Standardizing common header names (e.g., "Title" → "title", "Price (USD)" → "price_usd", "Model Name" → "model")

3. Added comprehensive test coverage using pytest:
   - Unit tests for individual cleaning functions
   - Integration tests for the complete cleaning pipeline
   - Tests using both file-based and StringIO-based approaches

4. Verified that all completion criteria are met:
   - `uv run glyphsieve clean --input foo.csv --output bar.csv` works as expected
   - `--dry-run` prints a mapping of the detected header transformation
   - Test coverage is present and can be run with `uv run pytest`

The implementation is now ready for use in downstream processing tasks.
