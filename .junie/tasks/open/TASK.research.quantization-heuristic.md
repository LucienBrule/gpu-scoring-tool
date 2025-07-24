# TASK.research.quantization-heuristic.md

## 🧩 Task: Develop Quantization Capability Heuristic

Junie, your task is to implement a heuristic function that flags GPU listings as “quantization-capable” based on key characteristics derived from metadata. This tag will help identify cards well-suited for low-bit inference workloads like LoRA or quantized LLMs (e.g. 4-bit 70B models).

---

## 🎯 Objectives

- Implement a method to classify listings as:
  - `quantization_capable: true | false`
- Integrate this into the `enrich` step or as a standalone field augmentation step
- Add a new column to the enriched or scored CSVs: `quantization_capable`

---

## 📐 Heuristic Criteria (Initial Rules)

Flag a GPU as `quantization_capable = true` if **all** of the following are met:

- `vram_gb >= 24`
- `tdp_watts <= 300` (power efficiency threshold)
- `mig_support = true` (enables model partitioning or parallel inference)

You **must** expose these thresholds as a configurable, overridable `Pydantic` model that is loadable from a YAML config file.
This config should live in `resources/quantization_heuristic.yaml` and conform to a structured DTO.
It should also be constructable in-code for dynamic use and testability.

Additionally, the heuristic logic must follow the **strategy pattern**:
- Define an abstract base class (ABC) for heuristic taggers
- Each heuristic must accept a structured row represented as a DTO (Pydantic model)
- Return a key:value output suitable for inclusion in the final dataset
- All outputs must conform to supported output types: boolean, integer, float, or string (enum)

This enables consistent tagging, runtime evaluation, and future extension to other heuristic types (e.g. `underpowered`, `rack_friendly`, etc.)

---

## 📦 Implementation Details

- Logic lives in `glyphsieve/core/heuristics.py`
- If integrated into enrich step: apply tag before scoring
- If standalone: add `glyphsieve tag-quantization` as CLI command

---

## 🧪 Tests

- Create test cases for:
  - GPUs that meet the criteria
  - GPUs that narrowly miss (e.g. 20 GB VRAM)
  - Boundary values (e.g. 24 GB, 301W TDP, no MIG)

- Place tests in `glyphsieve/tests/test_heuristics.py`

---

## ✅ Completion Criteria

- A new field `quantization_capable` is present in enriched or scored datasets
- CLI support is available (if implemented as command)
- Tests validate expected behavior and edge cases
- Heuristic logic is documented or visualized in comments

---

## ✍️ Notes

This capability is a key classifier for identifying GPUs suitable for quantized LLM hosting or multi-session low-bit inference. It informs rack design, power budgeting, and deal evaluation.