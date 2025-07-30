

# TASK.loader.01.define-source-loader-interface

## Summary

Establish a pluggable, abstract interface for defining structured data extractors ("source loaders") used to ingest data from vendor-specific APIs, exports, or other unconventional formats. This lays the foundation for flexible ingest pipelines that can translate third-party formats into pipeline-compatible CSV inputs.

## Motivation

To prepare for ingestion of diverse data sources (e.g. Shopify, REST APIs, flat JSON files), we need a common interface that encapsulates data extraction, normalization, and optional filtering. This enables the CLI pipeline and API systems to delegate the conversion process to purpose-built loaders. Each loader must emit a CSV-compatible schema (e.g. matching `input.csv`) for downstream stages.

## Scope

This task defines:
- An abstract `SourceLoader` interface in `glyphsieve.core.ingest.base_loader` (or similar)
- Clear method contracts for:
  - `load(source: str | Path) -> list[dict]` (load raw source)
  - `to_input_csv(rows: list[dict], output_path: Path)` (emit to input format)
- One minimal stub implementation `DummySourceLoader` for testing only

This task does *not* include:
- Shopify-specific logic
- Real ingest transforms
- CLI or API binding (deferred to later tasks)

## Implementation Requirements

- Use ABC module to enforce interface structure
- Include a `registry` pattern or plugin surface for loader registration
- Prepare interface for future multi-mode loaders (e.g. `load_live()` for networked APIs)
- Include one test in `tests/test_source_loader.py` validating interface behavior with dummy data

## Developer Experience

```
# Example interface usage

loader = DummySourceLoader()
data = loader.load("example.json")
loader.to_input_csv(data, Path("out.csv"))

# Future CLI hook
uv run glyphsieve pipeline --source shopify --supplier wamatek --input raw.json
```

## Acceptance Criteria

- [ ] `SourceLoader` is defined with appropriate ABC and docstrings
- [ ] Dummy implementation works and test is passing
- [ ] Module structure supports future plugin growth
- [ ] Task is lint-clean, test-passing, and patchable by Junie

## References

- EPIC.loader.shopify-source-loader
- TASK.loader.02.define-shopify-json-loader
- TASK.loader.03.load-shopify-wamatek-json
- pipeline: glyphsieve.pipeline.input_csv_loader