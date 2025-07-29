
# Task: pipeline.add-scoring-engine-v1.2

## Objective
Refactor the GPU scoring engine to consume enriched dataset outputs, integrate quantization capacity metrics, and apply dynamic, weighted scoring based on enriched metadata and configuration.

## Context
The existing scoring engine operates on normalized raw data and uses hard-coded weight values. To align with the new enrichment pipeline:
- It must accept Pydantic-modeled enriched records.
- It needs to load scoring weights and heuristics from the centralized resource registry.
- Quantization capacity (calculated in pipeline.quantization-capacity-metric) must influence final scores.

## Requirements
1. **Input Model**  
   - Consume enriched rows represented by the `EnrichedGPU` Pydantic model. Each record includes:
     - `model: str`, `vram_gb: float`, `tdp_watts: float`, `mig_capacity: float`, `nvlink_supported: bool`, plus any additional enriched fields.

2. **Weight Configuration**  
   - Load scoring weights via the `YamlLoader` abstraction from `glyphsieve.resources`.
   - Support override flags for each weight (`--weight-vram`, `--weight-mig`, `--weight-nvlink`, `--weight-tdp`, `--weight-price`) for ad-hoc tuning.

3. **Score Calculation**  
   - Compute a **raw score** as a weighted sum:
     ```
     raw_score = (
       weight_vram * vram_gb_normalized +
       weight_mig * mig_capacity_normalized +
       weight_nvlink * (1 if nvlink_supported else 0) +
       weight_tdp * (1 / tdp_watts_normalized) +
       weight_price * (1 / price_normalized)
     )
     ```
   - Incorporate the **quantization score** from the previous pipeline stage:
     ```
     adjusted_score = raw_score * (1 + quantization_score)
     ```
   - Normalize the final score to a 0–100 scale across all records.

4. **Output Model & Serialization**  
   - Map results to a `ScoredGPU` Pydantic model with fields:
     - `model: str`
     - `raw_score: float`
     - `quantization_score: float`
     - `final_score: float`
   - Serialize output to CSV via `csv.DictWriter`, including headers:
     ```
     model,raw_score,quantization_score,final_score
     ```

5. **CLI Integration**  
   - Add or update CLI command:
     ```
     uv run pipeline.score
       --input <enriched_csv>
       --output <scored_csv>
       [--weight-vram <float> ...]
     ```
   - Ensure the command uses the new loader interfaces and Pydantic models.

## Acceptance Criteria
- **Unit Tests**: Extend `glyphsieve/tests/test_scoring.py` to cover:
  - Weight-loading from YAML.
  - Correct raw_score and adjusted_score calculations.
  - Overrides via CLI flags.
- **End-to-End**: Running:
  ```
  uv run pipeline.enrich --input sample/normalized.csv --output sample/enriched.csv
  uv run pipeline.quantization-capacity --input sample/enriched.csv --output sample/enriched_q.csv
  uv run pipeline.score --input sample/enriched_q.csv --output sample/scored.csv
  ```
  should produce a `sample/scored.csv` with valid `ScoredGPU` rows.
- **Lint & Types**: All new code passes GLS lint rules and MyPy type checks.
- **Documentation**: Update `docs/architecture/pipeline.md` with the new scoring step overview.

## ✅ Task Completed

**Changes made:**
- Implemented the `ScoredGPU` Pydantic model for the output format
- Created the `EnhancedWeightedScorer` strategy that incorporates quantization capacity
- Implemented weight loading from YAML using the `YamlLoader` abstraction
- Added CLI flags for weight overrides (`--weight-vram`, `--weight-mig`, etc.)
- Implemented score calculation with raw score, quantization score, and final score
- Normalized final scores to a 0-100 scale
- Added CSV serialization using `csv.DictWriter`
- Updated the pipeline CLI to include quantization capacity
- Created documentation in `docs/architecture/pipeline.md`
- Fixed failing tests to work with the new scoring engine output format
- Ensured all code passes linting checks

**Outcomes:**
- The scoring engine now consumes enriched dataset outputs
- Quantization capacity metrics are integrated into the scoring
- Dynamic, weighted scoring is applied based on enriched metadata
- Weight configuration can be loaded from YAML and overridden via CLI flags
- All tests pass, including the pipeline integration tests
- Documentation is updated with the new scoring step overview

**Lessons learned:**
- Pydantic models provide a clean way to define input and output formats
- The Strategy pattern allows for flexible scoring algorithms
- YAML configuration makes it easy to adjust weights without code changes
- CLI flags provide a convenient way to override weights for ad-hoc tuning

**Follow-up needed:**
- Consider adding more scoring strategies for different use cases
- Add more comprehensive tests for edge cases
- Consider performance optimizations for large datasets