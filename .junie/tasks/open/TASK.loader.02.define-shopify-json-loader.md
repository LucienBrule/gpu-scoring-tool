

### 🧩 Task Title

Define Shopify JSON Loader

---

### 📍 Epic

[EPIC.loader.shopify-source-loader.md](../epics/open/EPIC.loader.shopify-source-loader.md)

---

### 📜 Description

Create a loader implementation for Shopify JSON data sources. This loader will parse Wamatek-style product listing exports (currently saved in the `recon/` directory) and transform them into a standardized format suitable for ingestion by the GPU Scoring Tool pipeline (e.g. `input.csv` compatible format).

This loader should serve as the concrete implementation of the abstract Shopify loader interface defined in TASK.loader.01. It must support parsing JSON structures from local files (initially), and yield well-formed entries with the following inferred fields:

- `model` – extracted from product title or variant
- `condition` – inferred from tags or descriptions (e.g. “Refurbished”, “New”)
- `price` – extracted from price field (USD)
- `quantity` – inventory quantity (if available)
- `source_url` – link to the Shopify product
- `source_type` – statically set to `Shopify_Wamatek`
- `title` – product title
- `geographic_region` – default to “USA”
- `listing_age` – set to `"Current"`
- `seller` – static value `"Wamatek"`

Use heuristics as needed to extract missing fields from description text, tags, or titles.

---

### ✅ Acceptance Criteria

- A concrete class `WamatekShopifyLoader` is implemented in the `glyphsieve.ingest.shopify` module.
- The loader reads JSON input and outputs a list of Pydantic-compatible DTOs (e.g. `RawListingDTO` or `dict`).
- Fuzzy title parsing and heuristics extract key fields such as `model`, `condition`, and `price`.
- The loader gracefully handles missing or malformed fields.
- Sample input file from `recon/wamatek_listings.json` is parsed and validated.
- Tests for loader behavior and corner cases are added under `glyphsieve/tests/`.

---

### 🧪 Dev Loop

You may use the following loop during development:

```bash
uv run glyphsieve shopify-parse --input recon/wamatek_listings.json --output demo/input.csv
pytest glyphsieve/tests/test_shopify_loader.py
```

---

### 🔗 Related Tasks

- [TASK.loader.01.define-source-loader-interface.md](./TASK.loader.01.define-source-loader-interface.md)
- [TASK.loader.03.load-shopify-wamatek-json.md](./TASK.loader.03.load-shopify-wamatek-json.md)
