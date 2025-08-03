

## TASK.ml.11.configure-ml-inference-via-yaml

This task implements configuration loading for ML-based inference during normalization. The goal is to make the classifier’s threshold, model path, and other inference options configurable using the existing `YamlLoader` system and loaded from a typed resource model.

---

### 📌 Purpose

Right now, the ML classifier is invoked with hardcoded parameters (e.g., fixed threshold, model path). This task externalizes these choices into a YAML config file (e.g., `ml_config.yaml`) so future tuning or variants can be swapped in without editing code.

---

### 📂 Implementation

- Add a file to `glyphsieve/resources/configs/ml_config.yaml` with initial structure:
  ```yaml
  model_path: models/gpu_classifier.pkl
  threshold: 0.2
  enabled: true
  ```

- Create a new Pydantic model in `glyphsieve/models/ml_config.py`:
  ```python
  from pydantic import BaseModel

  class MLConfig(BaseModel):
      model_path: str
      threshold: float = 0.2
      enabled: bool = True
  ```

- Load the config inside `ml_signal.py` via the existing `YamlLoader`:
  ```python
  from glyphsieve.resources.loader import YamlLoader
  from glyphsieve.models.ml_config import MLConfig

  config = YamlLoader().load(MLConfig, "configs/ml_config.yaml")
  ```

- Apply the threshold from `config.threshold` during classification filtering.
- Use `config.enabled` to allow bypassing the ML stage entirely if set to false.
- Update any CLI that uses ML (e.g. `--use-ml`) to honor this config or override it explicitly.

---

### 🔍 Acceptance Criteria

- `ml_config.yaml` is loaded correctly via YamlLoader
- All parameters are respected: model path, threshold, enabled flag
- If `enabled: false`, ML stage is skipped cleanly
- Threshold can be changed to adjust prediction filtering
- The config is documented inline and discoverable by agents
- Unit tests verify config parsing and conditional logic in `ml_signal.py`

---

### 🔗 Dependencies

- TASK.ml.04.integrate-ml-into-normalizer must be complete
- Requires model to already exist at configured path

---

### 🧪 Tests

- Add unit test in `tests/test_ml_config.py` validating:
  - Successful config load
  - Disabled config skips inference
  - Threshold is correctly passed

---

### 🔁 Future Ideas

- Multiple configs per model variant (e.g., `fast`, `accurate`, `v2`)
- Embedding-based thresholds or confidence bands

---

## ✅ Task Completed

**Changes made:**
- Created ML configuration infrastructure with `ml_config.yaml` and `MLConfig` Pydantic model
- Implemented `GlyphSievePklLoader` for loading pickle files from glyphsieve resources
- Moved `gpu_classifier_v2.pkl` model to `glyphsieve/src/glyphsieve/resources/models/`
- Updated `predictor.py` to use configuration-based model loading instead of environment variables
- Created `ml_signal.py` module that respects configuration settings (enabled/disabled, threshold)
- Added comprehensive tests in `test_ml_config.py` covering all configuration scenarios
- Updated existing `test_ml_integration.py` tests to work with new configuration system

**Outcomes:**
- ML inference is now fully configurable via YAML configuration files
- Model loading uses the resource loader pattern consistent with other glyphsieve components
- All configuration parameters (model_path, threshold, enabled) are respected
- ML stage can be cleanly disabled via configuration
- Both glyphsieve and glyphd lint clean (except pre-existing issues)
- All tests pass: 202 glyphsieve tests + 52 glyphd tests

**Lessons learned:**
- Configuration-based approach provides better flexibility than environment variables
- Resource loader pattern ensures packaging-safe model access
- Comprehensive test updates were needed to maintain compatibility with new architecture

**Follow-up needed:**
- None - task is complete and all acceptance criteria met