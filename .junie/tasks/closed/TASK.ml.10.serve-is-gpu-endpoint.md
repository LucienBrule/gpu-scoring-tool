

## TASK.ml.10.serve-is-gpu-endpoint

### 🎯 Goal

Expose a REST endpoint under `/api/ml/is-gpu` that accepts a JSON payload with a `title` field and returns the ML classifier's prediction (`ml_is_gpu` and `ml_score`) as a response.

This enables the GPU classifier to be used by external agents and crawlers (e.g., real-time scraping pipelines) for live inference.

### 🧠 Context

We have a trained model (`models/gpu_classifier.pkl`) that can classify GPU listings using only the `title` field.

This task creates a minimal serving layer inside `glyphd/` to expose the classifier via FastAPI.

### 📋 Requirements

- Endpoint: `POST /api/ml/is-gpu`
- Input: JSON body with field `title` (string)
- Output: JSON with:
  - `ml_is_gpu`: bool
  - `ml_score`: float (0–1)
- Load classifier on startup from disk
- Validate request payload using Pydantic
- Add test to `test_api_persist.py` to verify classifier output format

### 🗃️ Dependencies

- Requires `models/gpu_classifier.pkl` from `TASK.ml.02.train-binary-gpu-classifier`
- Uses ML model loaded from file via `joblib`
- ML logic must be encapsulated in a helper in `glyphsieve/ml/inference.py`

### ✅ Completion Criteria

- Endpoint responds correctly to valid input
- Includes appropriate FastAPI docs (summary/description)
- Rejects invalid/malformed requests
- Test coverage is added for request/response cycle
- Lints and tests clean

### 📎 Related

- EPIC: `EPIC.ml.ml-classifier-integration.md`
- TASK.ml.02 – training
- TASK.ml.04 – pipeline integration
- TASK.ml.09 – CLI wrapper

## ✅ Task Completed

**Changes made:**
- Created Pydantic models for ML API requests/responses in `glyphd/src/glyphd/api/models/ml.py`
- Implemented `/api/ml/is-gpu` POST endpoint in `glyphd/src/glyphd/api/routes/ml.py`
- Updated FastAPI router to include ML routes with proper OpenAPI tags
- Refactored `glyphsieve/ml/predictor.py` to use singleton ModelCache pattern instead of global variables
- Added comprehensive test coverage (6 test cases) in `test_api_persist.py`

**Outcomes:**
- REST endpoint successfully exposes ML classifier via FastAPI
- Endpoint accepts JSON with `title` field and returns `ml_is_gpu` (bool) and `ml_score` (float 0-1)
- Proper request validation using Pydantic models
- Graceful fallback when model file is unavailable (returns False, 0.0)
- All tests pass (10/10) including edge cases and validation scenarios
- Code lints clean after running isort, black, ruff, and flake8

**Lessons learned:**
- Singleton pattern provides better encapsulation than global variables for model caching
- FastAPI dependency injection works well with existing glyphsieve ML predictor functions
- Comprehensive test coverage is essential for API endpoints to handle edge cases

**Follow-up needed:**
- None - task fully completed and meets all requirements