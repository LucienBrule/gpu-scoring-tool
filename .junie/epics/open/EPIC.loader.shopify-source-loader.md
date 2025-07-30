

# EPIC: Shopify Source Loader Integration

## Status
OPEN

## Context
We’ve begun integrating real-world GPU listings into the pipeline, starting with JSON exports scraped from Wamatek’s Shopify API. These listings offer valuable signals that can be used to generate structured inputs for the scoring pipeline. To support this and future expansions (e.g. other Shopify sellers, Newegg, eBay APIs), we need a modular ingestion layer built around pluggable source loaders.

This epic will establish the Shopify Loader system and its associated plugin architecture.

## Goals

- Introduce a `SourceLoader` abstract interface to represent the transformation of arbitrary vendor exports into `input.csv` format.
- Define a `ShopifyLoader` base implementation for working with JSON-based Shopify APIs.
- Implement a `WamatekShopifyLoader` to support the specific JSON export format captured in `recon/wamatek.json`.
- Enable CLI invocation of loaders via pipeline pre-processing hooks.
- Preserve CLI UX: a user should be able to run:

```bash
uv run glyphsieve pipeline --source shopify --supplier wamatek --input recon/wamatek.json --output out.csv
```

...and have the correct loader selected and invoked automatically to produce a valid input.csv file.

## Tasks

- [ ] `TASK.loader.01.define-source-loader-interface.md`
- [ ] `TASK.loader.02.define-shopify-json-loader.md`
- [ ] `TASK.loader.03.load-shopify-wamatek-json.md`

## Acceptance Criteria

- Running the loader independently produces valid pipeline input.
- SourceLoader system supports additional vendors with minimal boilerplate.
- Junie can complete each task in isolation and compose into the CLI pipeline.
- Documentation and test coverage exist for loader registration and behavior.

## Agent Guidance

Junie:
- Do not hardcode anything about Wamatek in the abstract layers.
- Assume new vendors will be added.
- Loader output must match `input.csv` schema expected by the pipeline.
- If you're unsure, refer to sample pipeline input/output.

## Notes

- This system may evolve into a larger ingestion engine later, but for now it should be kept simple and composable.
- Consider compatibility with future daemon-oriented or streaming ingestion modes.

---

🧱 Once complete, this epic enables ingestion from live external vendor APIs.