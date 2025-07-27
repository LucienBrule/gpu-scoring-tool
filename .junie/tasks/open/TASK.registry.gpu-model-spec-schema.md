

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
   - Define a schema (as a Pydantic model) for `GPUModelSpec` including:
     - `name`: str — Canonical model name
     - `vram_gb`: int
     - `tdp_w`: int
     - `slots`: int
     - `mig_capable`: bool
     - `form_factor`: Literal["SFF", "Dual", "Triple", "FullHeight", ...]
     - `connectivity`: Optional[str] (e.g. PCIe 4.0, NVLink, SXM)
     - `notes`: Optional[str]
   - Use Pydantic v2 for all schema definitions

2. **YAML Loading**
   - Define a `GPUModelRegistry` container class that loads a set of YAML files and indexes them by canonical name
   - Implement validation and helpful error messages if malformed or missing fields are encountered
   - Add sample `gpu_models.yaml` file with ~10 sample entries to test loading

3. **Integration**
   - Implement CLI command `glyphsieve registry list` that prints the loaded registry as a formatted table
   - This command should use the YAML registry, load it via Pydantic, and pretty-print using standard library tools (no external deps)

4. **Test Coverage**
   - Add `test_registry.py` under `tests/` in `glyphsieve`
   - Include:
     - Registry loads correctly with valid input
     - Fails gracefully with invalid YAML
     - Canonical names are retrievable and accurate

5. **Guidelines Update**
   - Update `guidelines.md` to include instruction for adding new entries to the GPU registry YAML

## Bonus
- Add a method to return the closest matching GPU name in the registry (e.g., using Levenshtein distance)
- Implement support for vendor-specific aliases or marketing names (e.g. “RTX 6000 ADA” vs “RTX A6000”)

## Completion Criteria
- All requirements implemented and committed
- Tests pass via `uv run pytest`
- Running `glyphsieve registry list` prints the expected table
- Registry YAML lives in a durable place (e.g. `glyphsieve/registry/data/gpu_models.yaml`)
- Bonus (if implemented) documented in a docstring or help message