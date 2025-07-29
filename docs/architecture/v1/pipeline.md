# GPU Scoring Pipeline Architecture

This document provides an overview of the GPU scoring pipeline architecture in the glyphsieve project.

## Pipeline Overview

The GPU scoring pipeline consists of several stages that transform raw GPU listings into scored, enriched data:

1. **Clean**: Clean and standardize CSV headers
2. **Normalize**: Normalize GPU model names to canonical forms
3. **Deduplication** (optional): Remove duplicate listings
4. **Enrich**: Enrich listings with GPU metadata
5. **Quantization Capacity** (optional): Calculate quantization capacity for each GPU
6. **Score**: Score GPUs based on utility metrics

## Pipeline Stages

### 1. Clean

The cleaning stage standardizes CSV headers and ensures consistent column naming:

- Maps variant headers to standard names (e.g., "GPU Model" → "title")
- Handles case sensitivity and whitespace
- Ensures required columns are present

### 2. Normalize

The normalization stage maps raw GPU titles to canonical model names:

- Uses exact, regex, and fuzzy matching
- Assigns confidence scores to matches
- Outputs normalized data with canonical model names

### 3. Deduplication (Optional)

The deduplication stage identifies and removes duplicate listings:

- Groups by canonical model
- Uses price and other attributes to identify duplicates
- Marks primary and secondary listings

### 4. Enrich

The enrichment stage adds metadata to each GPU listing:

- Loads GPU specifications from a central registry
- Adds VRAM, TDP, MIG support, NVLink, and other attributes
- Preserves original data while adding enriched fields

### 5. Quantization Capacity (Optional)

The quantization capacity stage calculates how many models of different sizes can fit on each GPU:

- Calculates capacity for 7B, 13B, and 70B parameter models
- Accounts for VRAM overhead
- Adds quantization capacity metrics to enriched data

### 6. Score

The scoring stage evaluates GPUs based on utility metrics:

- **Input**: Enriched GPU listings with optional quantization capacity
- **Process**:
  - Calculates raw scores based on weighted attributes (VRAM, MIG, NVLink, TDP, price)
  - Incorporates quantization capacity into the scoring
  - Normalizes final scores to a 0-100 scale
- **Output**: Scored GPU listings with:
  - `model`: Canonical model name
  - `raw_score`: Raw score before quantization adjustment
  - `quantization_score`: Score adjustment based on quantization capacity
  - `final_score`: Final score after all adjustments (0-100 scale)

#### Scoring Weights

The scoring engine uses configurable weights for different attributes:

- `vram_weight`: Weight for VRAM capacity (higher is better)
- `mig_weight`: Weight for MIG support (higher is better)
- `nvlink_weight`: Weight for NVLink support (binary)
- `tdp_weight`: Weight for TDP (inverse, lower is better)
- `price_weight`: Weight for price (inverse, lower is better)
- `quantization_weight`: Weight for quantization capacity (higher is better)

These weights can be configured via a YAML file or overridden via CLI flags.

## CLI Usage

The pipeline can be run as a single command or as individual stages:

```bash
# Full pipeline
uv run glyphsieve pipeline --input raw.csv --output scored.csv --quantize-capacity

# Individual stages
uv run glyphsieve clean --input raw.csv --output cleaned.csv
uv run glyphsieve normalize --input cleaned.csv --output normalized.csv
uv run glyphsieve enrich --input normalized.csv --output enriched.csv
uv run glyphsieve quantization-capacity --input enriched.csv --output enriched_q.csv
uv run glyphsieve score --input enriched_q.csv --output scored.csv --weight-vram 0.3
```

## Extending the Pipeline

The pipeline is designed to be extensible:

- New scoring strategies can be added by implementing the `ScoringStrategy` interface
- New heuristics can be added by implementing the `Heuristic` interface
- New pipeline stages can be added by implementing new CLI commands

## Future Improvements

- Add more scoring strategies for different use cases
- Implement more heuristics for specialized domains
- Add support for more GPU attributes and features

## Demo Run

A full example run of the GPU scoring pipeline is available under `glyphsieve/demo`.

This demo includes:
- ✅ A cleaned input sample: `input.csv`
- 📦 Intermediate files per stage:
  - `stage_clean.csv`
  - `stage_normalized.csv`
  - `stage_enriched.csv`
  - `stage_quantized.csv`
- 📈 Final scored output: `output.csv`
- 📜 A Bash script to run the full pipeline: `run.sh`
- 📄 Terminal output log: `stdout.txt`

### To Run:

```bash
bash glyphsieve/demo/run.sh
```

This will execute the full `glyphsieve pipeline` command using the included input and emit enriched, quantized, and scored listings. Results will be saved in `glyphsieve/demo/output.csv`.

The demo confirms:
- End-to-end CLI integration is working
- All enrichment and scoring logic produces expected values
- The pipeline handles real-world header normalization and model canonicalization