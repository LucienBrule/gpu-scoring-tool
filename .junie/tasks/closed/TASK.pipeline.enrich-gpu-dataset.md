# TASK.pipeline.enrich-gpu-dataset.md

## Title
Implement GPU Listing Enrichment Pipeline Stage

---

## Persona
**You are the Enrichment Maestro**, responsible for ensuring each GPU listing is enriched with authoritative metadata. This stage is critical for downstream scoring: without accurate `vram_gb`, `mig_capable`, and `tdp_w`, scores will be invalid. Improvements are welcome, but do **not** break existing CLI flags or API surfaces.

---

## Purpose
Enrich normalized GPU listings by joining them with the canonical GPU Model Registry. This creates the essential dataset for accurate scoring and reporting.

---

## Requirements

1. **Enrichment Logic**
   - Implement `enrich_listings(records: List[GPUListingDTO]) -> List[EnrichedGPUListingDTO]`
   - **Use** the `ResourceContext` loader to fetch `GPUModelSpec` from `gpu_specs.yaml`
   - Do **not** perform fuzzy or alias matching in this task
   - Ensure each output record includes:
     - `vram_gb`, `mig_capable`, `slots`, `form_factor`, `tdp_w`
     - Any additional `notes` or `warnings` if metadata mismatch occurs

2. **DTO Definition**
   - Define a new `EnrichedGPUListingDTO` in `glyphsieve.models` or `dto/`
   - Do **not** mutate or overload `GPUListingDTO`
   - Validate enriched fields via Pydantic

3. **CLI Integration**
   - Add `@app.command("enrich")` to `glyphsieve.cli`
   - Flags:
     - `--input <path>` (existing normalized CSV; must exist and be readable)
     - `--output <path>` (enriched CSV; create parent dir if needed)
   - On success, print:  
     ```
     ✅ Enrichment complete: enriched CSV → <output>
     ```

4. **Pipeline Compatibility**
   - Output CSV must serve as valid input for `glyphsieve score`
   - Do **not** alter column order expected by scoring

5. **Testing**
   - Write unit tests in `glyphsieve/tests/test_enrichment.py`:
     - Verify enrichment logic for known inputs
     - Handle missing or invalid model names gracefully
   - Add CLI tests in `glyphsieve/tests/test_cli_pipeline.py` using `CliRunner`:
     - Happy path: generates correct CSV columns
     - Error path: missing input file → clear error message

---

## Manual Verification

```bash
# Run enrichment on sample data
uv run glyphsieve enrich \
  --input sample/sample_normalized.csv \
  --output sample/sample_enriched.csv

# Inspect first 5 lines
head -n 5 sample/sample_enriched.csv
```

---

## DX Runbook

After implementation, execute:

```bash
# Formatting & Imports
uv run black glyphsieve/src
uv run isort glyphsieve/src

# Linting
uv run ruff glyphsieve/src
uv run flake8 glyphsieve/src

# Run tests
uv run pytest glyphsieve/tests
```

All commands must complete with **zero errors**.

---

## Completion Criteria

- `glyphsieve enrich` command exists with correct help text
- Enrichment logic uses `ResourceContext` loader and new `EnrichedGPUListingDTO`
- Output CSV includes required fields and is compatible with scoring
- Manual verification commands produce expected results
- Unit and CLI tests cover both success and error flows
- Formatting and linting pass without any violations

## ✅ Task Completed

**Changes made:**
- Implemented `EnrichedGPUListingDTO` in `glyphsieve/src/glyphsieve/models/gpu.py` with all required fields and Pydantic validation
- Created `enrich_listings` function in `glyphsieve/src/glyphsieve/core/enrichment.py` that:
  - Uses `ResourceContext` loader to fetch GPU specs from `gpu_specs.yaml`
  - Joins listings with specs based on canonical model name
  - Adds metadata fields like vram_gb, tdp_w, mig_capable, slots, form_factor
  - Adds warnings for models not found in the registry
- Updated `enrich_csv` function to preserve original columns while adding enriched fields
- Added CLI command `enrich` in `glyphsieve/src/glyphsieve/cli/enrich.py` with required flags
- Created sample data in `sample/sample_normalized.csv` for testing
- Added comprehensive unit tests in `glyphsieve/tests/test_enrichment.py`
- Added CLI tests in `glyphsieve/tests/test_cli_pipeline.py`
- Fixed test failures and ensured all tests pass
- Verified implementation with manual verification commands

**Outcomes:**
- All 65 tests pass with zero errors
- Manual verification commands produce expected results
- Enrichment pipeline stage is fully functional and compatible with the rest of the pipeline
- Output CSV includes all required fields and is compatible with scoring

**Lessons learned:**
- Pandas DataFrame handling requires careful attention to boolean types (np.True_ vs True)
- Mock assertions need to be flexible when dealing with absolute vs relative paths
- Rich console formatting can affect test assertions that check for exact string matches

**Follow-up needed:**
- Consider adding more GPU models to the registry (A100_40GB_PCIE was not found)
- Consider adding fuzzy matching for model names in a future task