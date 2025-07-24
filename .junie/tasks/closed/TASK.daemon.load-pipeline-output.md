
# TASK.daemon.load-pipeline-output.md

## 🧩 Task: Load Pipeline Output into Glyphd Runtime State

Junie, your task is to implement a loader module in `glyphd` that reads pipeline outputs from the filesystem into in-memory DTOs, ready to be served via API endpoints.

This is the data ingestion layer for the daemon.

---

## 🎯 Objectives

- Implement functions to load:
  - `scored.csv` (final output from `glyphsieve pipeline`)
  - `Final_Market_Value_GPU_Summary.csv` (static GPU model metadata)
  - `insight.md` or its parsed `.json` variant (report output)

- Parse each input into structured DTOs and make them accessible to the API

---

## 📦 Location

Create a new module:

```
glyphd/
└── src/
    └── glyphd/
        └── core/
            └── loader.py
```

Define one function per input:

```python
def load_scored_listings(path: Path) -> list[GPUListingDTO]
def load_gpu_model_metadata(path: Path) -> list[GPUModelDTO]
def load_insight_report(path: Path) -> ReportDTO
```

You may use `pandas`, `csv`, or `orjson` for efficient loading.

---

## 🧪 Requirements

- All loaders must return validated DTOs using `pydantic` v2
- Handle missing or malformed fields gracefully
- Use `Path` from `pathlib`, not string paths
- Make paths configurable (for later service mode or CLI invocation)

---

## ✅ Completion Criteria

- Each loader function:
  - Accepts a file path
  - Returns structured, validated DTO(s)
  - Logs summary statistics (e.g., "Loaded 42 listings")

- You must wire these into FastAPI using **dependency injection**.
- Do not use global variables to store state.
- Use application lifecycle events (`startup`) or FastAPI dependencies to manage loaded data cleanly.

---

## ✍️ Notes

This loader layer forms the memory of the daemon. It must integrate with the FastAPI application lifecycle cleanly.
All components must use dependency injection and be built in a modular, testable way.
Avoid global state. Inject everything.

---

## 🏁 Task Completion Summary

Task completed on July 24, 2025. The following components were implemented:

1. **Core Loader Module**: Created `glyphd/src/glyphd/core/loader.py` with three functions:
   - `load_scored_listings()`: Loads GPU listings from CSV with score data
   - `load_gpu_model_metadata()`: Loads GPU model metadata with market statistics
   - `load_insight_report()`: Loads market insight reports from markdown or JSON

2. **Dependency Injection**: Created `glyphd/src/glyphd/core/dependencies.py` to:
   - Provide cached access to loaded data
   - Configure default file paths
   - Handle errors gracefully when files are missing

3. **API Integration**: Refactored `glyphd/src/glyphd/api/router.py` to:
   - Use dependency injection for data access
   - Remove hardcoded file paths
   - Simplify endpoint implementations

4. **Testing**: Added comprehensive tests in `glyphd/tests/test_loader.py` to verify:
   - Correct parsing of different file formats
   - Proper error handling for missing files
   - Data validation using Pydantic models

All tests are passing, confirming that the implementation meets the requirements. The code follows best practices for dependency injection and avoids global state, making it modular and testable.