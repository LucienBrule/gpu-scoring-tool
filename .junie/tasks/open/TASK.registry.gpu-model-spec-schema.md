# TASK.registry.gpu-model-spec-schema.md

## Title
Define GPU Model Registry Schema for Metadata Integration

## Category
registry

## Status
open

## Purpose
Introduce a canonical, structured registry of GPU model metadata to support normalization, enrichment, and scoring pipelines. This registry should live as structured YAML files loaded into Pydantic DTOs.

## Requirements

1. **Schema Design**
   - Define `GPUModelSpec` as a Pydantic v2 model with fields:
     - `name: str` — Canonical model name
     - `vram_gb: int`
     - `tdp_w: int`
     - `slots: int`
     - `mig_capable: bool`
     - `form_factor: str`  (use regex or a custom validator to validate form factor values)
     - `connectivity: Optional[str]` (e.g. PCIe 4.0, NVLink, SXM)
     - `notes: Optional[str]`
   - **Fields must use native types or `Annotated`, not Python `Enum`/`StrEnum` or raw string literals.**
   - **Registry YAML file must live at** `glyphsieve/resources/gpu_models.yaml`
   - **Access the YAML only via the `ResourceContext` loader**; direct `Path()` or file reads are disallowed (will be flagged by linter).

2. **YAML Loading via ResourceContext**
   - Implement `GPUModelRegistry` that uses `ResourceContext` to load `gpu_models.yaml` from `glyphsieve/resources/`
   - Index entries by `name`, raising `RuntimeError` on missing or malformed fields with clear messages
   - **Do not** use direct filesystem access

   **Example YAML entry** in `glyphsieve/resources/gpu_models.yaml`:
   ```yaml
   - name: "NVIDIA RTX 6000 Ada"
     vram_gb: 48
     tdp_w: 300
     slots: 2
     mig_capable: true
     form_factor: Dual
     connectivity: PCIe 4.0
   ```

3. **CLI Integration**
   - Add `@app.command("registry list")` in `glyphsieve.cli`
   - On invocation, load registry via `GPUModelRegistry`
   - **Print a tabular output** with columns:
     ```
     name               | vram_gb | mig_capable | tdp_w | slots | connectivity
     -------------------|---------|-------------|-------|-------|--------------
     NVIDIA RTX 6000 Ada| 48      | true        | 300   | 2     | PCIe 4.0
     ```
   - Use only stdlib formatting (e.g., `str.format` or `tabulate` from stdlib if available)

4. **Test Coverage & DX Runbook**
   - Create `glyphsieve/tests/test_registry.py` with:
     - Valid load test using sample YAML
     - Invalid YAML raises `RuntimeError` with expected message
     - Registry lookup by name returns correct `GPUModelSpec`
   - **DX Runbook**: After implementation, run:
     ```bash
     uv run black glyphsieve/src
     uv run isort glyphsieve/src
     uv run ruff glyphsieve/src
     uv run flake8 glyphsieve/src
     uv run pytest
     ```
   - All lint and test commands must finish with zero errors.

## Bonus
- **Implement fuzzy-matching alias logic (required)** leveraging existing matcher infrastructure.
- Implement support for vendor-specific aliases or marketing names (e.g. “RTX 6000 ADA” vs “RTX A6000”)

## Completion Criteria
- All requirements implemented and committed
- Tests pass via `uv run pytest`
- Running `glyphsieve registry list` prints the expected table
- `gpu_models.yaml` resides at `glyphsieve/resources/gpu_models.yaml`
- `glyphsieve registry list` prints the table as specified
- `ResourceContext` loader is used; no direct file access
- Linting and tests pass without violations
- **Tests for fuzzy-match alias functionality must be included, verifying that `closest_match` returns the nearest registry entry.**
- Bonus alias/closest-match logic, if added, is documented and tested