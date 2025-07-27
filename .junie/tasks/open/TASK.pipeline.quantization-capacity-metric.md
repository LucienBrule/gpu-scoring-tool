

# TASK.pipeline.quantization-capacity-metric.md

## Title
Estimate Quantization Capacity per Listing

## Category
pipeline

## Status
open

## Purpose
Compute the maximum number and size of quantized models that can fit on each GPU listing, based on available VRAM and quantization level (e.g., 4-bit models). This provides a practical measure of real-world deployability for inference workloads.

## Requirements

1. **Metric Definition**
   - For each listing, calculate:
     - How many 7B, 13B, and 70B models (4-bit quantized) can fit in VRAM
     - Assume ~1 byte = 2 bits of actual useable model memory
     - Factor in a 1–2 GB overhead for system / kernel / runtime usage
   - Example formula:
     - 7B @ 4bit ≈ 3.5 GB
     - 13B @ 4bit ≈ 6.5 GB
     - 70B @ 4bit ≈ 35–40 GB
     - Subtract overhead before division

2. **Implementation**
   - Add a `quantization_capacity` field or dict to each enriched listing
   - Format:
     ```json
     {
       "7b": 2,
       "13b": 1,
       "70b": 0
     }
     ```
   - Can live in a top-level field or a nested key under `heuristics`

3. **Heuristic Strategy**
   - Add a new strategy under the heuristic engine (strategy pattern)
   - This strategy evaluates listings with sufficient VRAM and populates the capacity dictionary

4. **Integration**
   - Add a CLI flag to `glyphsieve enrich` and/or `pipeline`:
     - `--quantize-metric` enables this stage
   - Ensure the resulting capacity metrics are included in final CSVs

5. **Testing**
   - Add tests for the heuristic to verify capacity numbers for known VRAM values
   - Test integration with `enrich` or `pipeline` commands

## Bonus
- Add a flag to show quantization metrics as a new column in the insight report
- Support other quantization levels (e.g., 8-bit)

## Completion Criteria
- Listings enriched with quantization capacity per model size
- Metrics appear in output CSVs when flag is passed
- Unit tests validate sizing logic for 4-bit models
- Integration tests ensure CLI output correctness