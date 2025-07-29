# TASK.pipeline.quantization-capacity-metric.md

## Title
Estimate Quantization Capacity per Listing

## Category
pipeline

## Status
open

## Persona
You are **the Quantization Oracle**, the guardian of VRAM-based model fitting. Your mission is to measure and annotate each GPU listing with precise quantization capacity, ensuring operators instantly understand deployable model counts.

## Purpose
Compute the maximum number and size of quantized models that can fit on each GPU listing, based on available VRAM and quantization level (e.g., 4-bit models). This provides a practical measure of real-world deployability for inference workloads.

## Requirements

1. **Quantization Capacity Metric**
   - Define a Pydantic model `QuantizationCapacitySpec` or similar in `glyphsieve.models.quantization` with fields:
     ```python
     class QuantizationCapacitySpec(BaseModel):
         "7b": int
         "13b": int
         "70b": int
     ```
   - Store VRAM requirements in `glyphsieve/resources/quantization_heuristic.yaml`:
     ```yaml
     overhead_gb: 2
     models:
       7b: 3.5
       13b: 6.5
       70b: 35.0
     ```
   - Load these constants via the `ResourceContext` loader; direct file or Path access is prohibited.
   - Compute:
     ```
     capacity = floor((vram_gb - overhead_gb) / model_vram_gb)
     ```
   - Capacity values must be non-negative integers.

2. **Implementation**
   - Extend `EnrichedGPUListingDTO` to include a field:
     ```python
     quantization_capacity: QuantizationCapacitySpec
     ```
   - Ensure Pydantic validation is applied; enriched DTO must import config-loaded model

3. **Heuristic Strategy**
   - Implement as a subclass of `BaseHeuristicStrategy`
   - Register strategy name `quantization_capacity`
   - Logic must compute and assign `quantization_capacity` on the DTO

4. **CLI Integration**
   - Add flag `--quantize-capacity` to `glyphsieve pipeline` (and/or `--quantize-capacity` on `enrich`)
   - When flag is absent, do not compute metric
   - If `quantization_capacity` already exists and flag not `--force-quantize`, exit with error
   - On success, print:
     ```
     ✅ Quantization capacity computed and added to output CSV → <output>
     ```

5. **Testing & DX Runbook**
   - Add unit tests in `glyphsieve/tests/test_quantization.py` for:
     - VRAM 14 GB → capacity 7b=3, 13b=1, 70b=0
     - VRAM 48 GB → capacity 7b=13, 13b=7, 70b=1
     - VRAM below overhead only → all zero
   - Add CLI tests in `glyphsieve/tests/test_cli_quantization.py`:
     - `uv run glyphsieve pipeline --quantize-capacity` adds the new DTO column
     - Omit flag → no quantization field present
     - Existing quantization field + no `--force-quantize` → clear error

   **Manual CLI Verification**
   ```bash
   uv run glyphsieve pipeline \
     --input sample/sample_enriched.csv \
     --output sample/sample_quant.csv \
     --quantize-capacity
   head -n 5 sample/sample_quant.csv
   ```

   **DX Runbook**
   ```bash
   uv run black glyphsieve/src
   uv run isort glyphsieve/src
   uv run ruff glyphsieve/src
   uv run flake8 glyphsieve/src
   uv run pytest
   ```
   All commands must complete with zero errors.

## Additional Requirement
- Compute and include `quantization_capacity` in the insight report as a new column when `--quantize-capacity` is passed.

## Completion Criteria
- Running `uv run glyphsieve pipeline --quantize-capacity --input sample/sample_enriched.csv --output sample/sample_quant.csv` produces an output CSV with a valid `quantization_capacity` column matching `QuantizationCapacitySpec`.
- The insight report includes the `quantization_capacity` column when `--quantize-capacity` is used.
- Unit tests for `QuantizationCapacitySpec` logic and CLI integration tests pass without errors.
- All linting and formatting commands (`uv run black`, `uv run isort`, `uv run ruff`, `uv run flake8`, `uv run pytest`) complete cleanly with zero violations.