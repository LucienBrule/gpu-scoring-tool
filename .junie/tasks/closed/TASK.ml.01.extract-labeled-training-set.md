## Persona
You are the Data Curator. Your role is to extract, clean, and prepare labeled training datasets from normalized GPU listings to enable machine learning model development.

## Title
Extract Labeled Training Set for GPU Binary Classification

## Purpose
Build a labeled training dataset from the existing `stage_normalized.csv` file to train a binary classifier that can identify NVIDIA GPUs. The dataset will be used to augment the current rule-based system and improve the last 2% accuracy gap in normalization.

## Requirements

1. **Data Extraction**
   - Read `tmp/work/stage_normalized.csv` (~10,530 rows)
   - Extract columns: `title`, `bulk_notes`, `canonical_model`
   - Create binary label `is_gpu` where:
     - `is_gpu = 1` if `canonical_model != "UNKNOWN"` AND is an NVIDIA GPU
     - `is_gpu = 0` otherwise (Intel, AMD, or unknown GPUs)

2. **Training Set Creation**
   - Build `training_set.csv` with columns: `title`, `bulk_notes`, `is_gpu`
   - Ensure data quality: remove rows with missing `title` or `bulk_notes`
   - Balance check: report class distribution (GPU vs non-GPU)

3. **Train/Test Split**
   - Perform 80/20 stratified split to maintain class balance
   - Generate `train.csv` (80% of data)
   - Generate `test.csv` (20% of data)
   - Use random seed for reproducibility

4. **Output Structure**
   - Create directory `glyphsieve/ml/data/` if it doesn't exist
   - Save all CSV files with proper headers
   - Use YAML format for metadata file
   - Include a `label_spec_version` field to describe the labeling logic version (e.g., "v1.0")
   - Include a count of skipped rows due to missing `title` or `bulk_notes`
   - Include metadata file `dataset_info.yaml` with:
     - Total rows processed
     - Class distribution
     - Train/test split sizes
     - Creation timestamp

## Constraints
- All ML code lives in `glyphsieve/ml/`; keep the rest of the project import-free from heavy libs
- Use only CPU-based processing; no cloud notebooks or CUDA dependencies
- No Jupyter/IPython artifacts; pure `.py` files only
- Follow existing project linting rules (ruff, flake8, GLS00X rules)
- Append columns; never reorder or drop existing ones from source data

## Tests
- **Unit tests** in `glyphsieve/tests/test_ml_data_extraction.py`:
  - Verify correct binary labeling logic for various `canonical_model` values
  - Test train/test split maintains proper stratification
  - Validate output CSV format and column names
- **Integration tests**:
  - End-to-end test with sample normalized CSV
  - Verify all output files are created with expected structure

## DX Runbook
```bash
# Create the training dataset
uv run glyphsieve ml-extract-training-set \
  --input tmp/work/stage_normalized.csv \
  --output glyphsieve/ml/data/

# Verify output files
ls -la glyphsieve/ml/data/
cat glyphsieve/ml/data/dataset_info.yaml

# Run tests
pytest glyphsieve/tests/test_ml_data_extraction.py -v

# Lint check
uv run ruff glyphsieve/ml/
uv run flake8 glyphsieve/ml/
```

## Completion Criteria
- `training_set.csv`, `train.csv`, and `test.csv` files created in `glyphsieve/ml/data/`
- Binary labels correctly assigned based on NVIDIA GPU identification
- 80/20 stratified split maintains class balance within 2%
- `dataset_info.yaml` contains accurate metadata, including labeling spec version and skipped row count
- All unit and integration tests pass
- Code passes all linting checks (ruff, flake8, GLS00X rules)
- CLI command `glyphsieve ml-extract-training-set` works as documented

## ✅ Task Completed

**Changes made:**
- Created ML module structure in `glyphsieve/src/glyphsieve/ml/`
- Implemented `data_extraction.py` with binary labeling using shared CANONICAL_MODELS logic
- Built `train_test_split.py` with stratified splitting functionality
- Created `services.py` for business logic separation from CLI concerns
- Implemented `cli_extract.py` with thin CLI interface delegating to service layer
- Generated all required output files: training_set.csv (10,530 rows), train.csv (8,424 rows), test.csv (2,106 rows), dataset_info.yaml
- Added comprehensive unit tests (29 tests) covering all functionality
- Fixed 11 additional failing tests across the codebase during integration

**Outcomes:**
- Successfully extracted labeled training dataset with 42.5% GPU samples (4,479 NVIDIA GPUs, 6,051 non-GPUs)
- Achieved perfect class balance preservation (max difference: 0.0001%)
- All tests pass (174 total, 0 failures)
- Code follows project architectural patterns and linting rules
- CLI integration complete with `uv run glyphsieve ml-extract-training-set`

**Lessons learned:**
- Using shared CANONICAL_MODELS from core.normalization ensures consistency with existing pipeline
- Service layer pattern provides clean separation between business logic and CLI presentation
- Stratified splitting with scikit-learn maintains class balance automatically
- Comprehensive testing caught integration issues early

**Follow-up needed:**
- TASK.ml.02: Train binary GPU classifier using the extracted dataset