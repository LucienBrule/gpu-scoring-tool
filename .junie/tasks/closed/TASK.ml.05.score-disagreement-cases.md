## Persona
You are the Quality Analyst. Your role is to identify discrepancies between different classification systems, surface edge cases for human review, and provide insights that improve overall system accuracy.

## Title
Identify and Score Rule-ML Disagreement Cases

## Purpose
Create a systematic approach to identify listings where the rule-based normalization system and ML classifier disagree. These disagreement cases represent potential improvements to either system and require analyst review to determine ground truth and system refinements.

## Requirements

1. **Disagreement Detection Logic**
   - Identify two types of disagreements:
     - **Type A**: Rules classify as `UNKNOWN` but ML predicts `is_gpu = 1`
     - **Type B**: Rules classify as known GPU (not `UNKNOWN`) but ML predicts `is_gpu = 0`
   - Apply disagreement detection to normalized CSV files with ML predictions
   - Calculate disagreement rate as percentage of total processed rows
   - Scoring weights and threshold values **must** be sourced from a YAML configuration file using the project's `YamlLoader`. Do not hardcode scoring logic.

2. **CLI Command Implementation**
   - Create CLI command: `glyphsieve ml-disagreements`
   - Parameters:
     - `--input`: path to normalized CSV with ML columns (required)
     - `--output`: path for disagreements CSV (default: disagreements.csv)
     - `--min-confidence`: minimum ML confidence threshold (default: 0.7)
       - Default is 0.7 — balances false negatives against analyst review workload.
     - `--max-rows`: limit output rows for large datasets (default: 1000)
   - Include progress indicators and summary statistics

3. **Disagreement Analysis Output**
   - Generate `disagreements.csv` with columns:
     - `title`, `bulk_notes`, `canonical_model`, `ml_is_gpu`, `ml_score`
     - `disagreement_type`: "rules_unknown_ml_gpu" or "rules_gpu_ml_unknown"
     - `confidence_level`: "high" (>0.8), "medium" (0.6-0.8), "low" (<0.6)
     - `priority_score`: ranking for analyst review (1-10 scale)
   - Sort by priority_score descending, then by ml_score
   - Optionally emit `disagreements_debug.json` for top N disagreements with full source row metadata for inspection.

4. **Summary Report Generation**
   - Create `disagreement_summary.md` with:
     - Total disagreements found and percentage of dataset
     - Breakdown by disagreement type and confidence level
     - Top-10 most confident disagreements for each type
     - Recommendations for system improvements
     - Statistical analysis of disagreement patterns

## Constraints
- Target disagreement rate <3% of total rows (per EPIC definition of done)
- All analysis code lives in `glyphsieve/ml/` directory
- No Jupyter/IPython artifacts; pure `.py` files only
- Follow existing project linting rules (ruff, flake8, GLS00X rules)
- Handle large datasets efficiently with streaming/chunking if needed
- Configurable thresholds and scoring weights should be loaded from a resource YAML file in future iterations to support tuning without code changes.
- Scoring configuration (e.g., priority weights) must be defined in a resource YAML file and loaded via the `YamlLoader` pattern.

## Tests
- **Unit tests** in `glyphsieve/tests/test_ml_disagreements.py`:
  - Test disagreement detection logic with known cases
  - Verify priority scoring algorithm
  - Test confidence level categorization
  - Validate CSV output format
  - Test that YAML-based configuration is loaded correctly and used in scoring logic.
- **Integration tests**:
  - End-to-end disagreement analysis with sample data
  - Test CLI command with various parameters
  - Verify summary report generation

## DX Runbook
```bash
# Run disagreement analysis on normalized data with ML
uv run glyphsieve ml-disagreements \
  --input tmp/work/normalized_with_ml.csv \
  --output tmp/analysis/disagreements.csv \
  --min-confidence 0.7

# Review disagreement summary
cat tmp/analysis/disagreement_summary.md

# Check high-priority disagreements
head -20 tmp/analysis/disagreements.csv

# Analyze disagreement patterns
uv run glyphsieve ml-disagreements \
  --input tmp/work/normalized_with_ml.csv \
  --output tmp/analysis/high_conf_disagreements.csv \
  --min-confidence 0.9 \
  --max-rows 100

# Run tests
pytest glyphsieve/tests/test_ml_disagreements.py -v

# Lint check
uv run ruff glyphsieve/ml/
uv run flake8 glyphsieve/ml/
```

## Completion Criteria
- CLI command `glyphsieve ml-disagreements` implemented and functional
- `disagreements.csv` generated with all required columns and proper sorting
- `disagreement_summary.md` provides comprehensive analysis and insights
- Disagreement rate <3% of total rows when run on full dataset
- Priority scoring helps analysts focus on most important cases
- High-confidence disagreements (>0.8) flagged for immediate review
- All unit and integration tests pass
- Code passes all linting checks (ruff, flake8, GLS00X rules)
- Performance acceptable for datasets up to 50k rows
- Documentation includes examples of disagreement types and resolution workflow
- Scoring behavior is driven by external YAML configuration loaded via YamlLoader.

## Glossary

- **Disagreement Type**:
  - `rules_unknown_ml_gpu`: Rules = UNKNOWN, ML = is_gpu 1
  - `rules_gpu_ml_unknown`: Rules = known GPU, ML = is_gpu 0

- **Confidence Level**:
  - `high`: ML score > 0.8
  - `medium`: 0.6 ≤ ML score ≤ 0.8
  - `low`: ML score < 0.6

- **Priority Score**:
  - A computed value (1–10) to help surface impactful disagreements. Higher = more urgent for review.