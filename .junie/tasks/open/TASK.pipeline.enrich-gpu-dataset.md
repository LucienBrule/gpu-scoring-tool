

# TASK.pipeline.enrich-gpu-dataset.md

## Title
Implement GPU Listing Enrichment Pipeline Stage

## Category
pipeline

## Status
open

## Purpose
This task implements the `enrich` stage of the pipeline. It is responsible for adding derived or externally joined metadata to raw listings, based on model name normalization and the registry schema.

## Requirements

1. **Create `enrich_listings` stage**
   - Takes in a list of `GPUListingDTO` objects from the normalized pipeline stage
   - Joins each listing with the `GPUModelSpec` metadata loaded from the GPU registry
   - Adds fields such as:
     - `vram_gb` (if not already present or inconsistent)
     - `mig_capable`, `slots`, `form_factor`, `tdp_w`
     - Any inferred tags or notes (if applicable)

2. **Integration**
   - Add an `@app.command("enrich")` to `glyphsieve.cli`
     - Accepts `--input` and `--output` paths
     - Runs enrichment and emits the resulting enriched CSV
   - Allow enriching a normalized CSV directly from CLI

3. **DTO Extension**
   - Define a new `EnrichedGPUListingDTO` or extend the existing DTO
   - Ensure enriched fields are present and validated
   - Avoid duplication of columns from raw input

4. **Testing**
   - Add unit tests for enrichment logic in `tests/enrichment/`
   - Add CLI integration tests with `CliRunner`

5. **Dependency**
   - This task assumes the GPU Model Registry schema is implemented (see: `TASK.registry.gpu-model-spec-schema.md`)

## Bonus
- Detect inconsistencies (e.g., claimed VRAM vs. actual model VRAM) and add a `warnings` field per listing
- Add a `source_match_score` field if fuzzy matching or alias resolution was used

## Completion Criteria
- The CLI command `glyphsieve enrich` works as described
- Given a normalized CSV, the output has new metadata columns as defined
- Tests pass for registry-based enrichment and CLI coverage
- DTOs are properly versioned and separated