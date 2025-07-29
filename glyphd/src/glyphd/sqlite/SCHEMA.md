# GPU Scoring Tool SQLite Schema

This document describes the SQLite schema for the GPU Scoring Tool. The schema is designed to store GPU listings, models, scored listings, and quantization data.

## Overview

The schema consists of the following tables:

1. `schema_version`: Tracks schema versions and migrations
2. `import_batches`: Tracks import batches and enables differential updates
3. `models`: Stores normalized GPU model registry with technical specifications
4. `listings`: Stores raw listing metadata parsed from CSV input
5. `scored_listings`: Stores enriched and scored GPU listings
6. `quantized_listings`: Stores quantization capacities for GPU listings

## Tables

### schema_version

Tracks schema versions and migrations.

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| id | INTEGER | No | AUTOINCREMENT | Primary key |
| version | TEXT | No | | Schema version (e.g., "1.0.0") |
| applied_at | TIMESTAMP | No | CURRENT_TIMESTAMP | When the schema version was applied |
| description | TEXT | Yes | | Description of the schema version |

### import_batches

Tracks import batches and enables differential updates.

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| id | INTEGER | No | AUTOINCREMENT | Primary key |
| import_id | TEXT | No | | User-provided ID for the import batch (unique) |
| imported_at | TIMESTAMP | No | CURRENT_TIMESTAMP | When the import batch was created |
| source | TEXT | Yes | | Source of the import (e.g., "csv", "api") |
| record_count | INTEGER | Yes | 0 | Number of records in this batch |
| description | TEXT | Yes | | Description of the import batch |

### models

Stores normalized GPU model registry with technical specifications.

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| id | INTEGER | No | AUTOINCREMENT | Primary key |
| model | TEXT | No | | Canonical model name (e.g., "H100_PCIE_80GB") (unique) |
| vram_gb | INTEGER | Yes | | VRAM capacity in GB |
| tdp_watts | INTEGER | Yes | | Thermal Design Power in watts |
| mig_support | INTEGER | Yes | 0 | MIG support level (0-7) |
| nvlink | BOOLEAN | Yes | 0 | NVLink support (0=false, 1=true) |
| generation | TEXT | Yes | | GPU architecture generation (e.g., "Hopper", "Ada") |
| cuda_cores | INTEGER | Yes | | Number of CUDA cores |
| slot_width | INTEGER | Yes | | Physical slot width |
| pcie_generation | INTEGER | Yes | | PCIe generation |
| listing_count | INTEGER | Yes | 0 | Number of listings for this model |
| min_price | REAL | Yes | | Minimum price for this model |
| median_price | REAL | Yes | | Median price for this model |
| max_price | REAL | Yes | | Maximum price for this model |
| avg_price | REAL | Yes | | Average price for this model |
| created_at | TIMESTAMP | No | CURRENT_TIMESTAMP | When the record was created |
| updated_at | TIMESTAMP | No | CURRENT_TIMESTAMP | When the record was last updated |
| import_id | TEXT | Yes | | Reference to the import batch |

**Indexes:**
- `idx_models_model`: Index on `model` for faster lookups

**Foreign Keys:**
- `import_id` references `import_batches(import_id)` with `ON DELETE SET NULL`

### listings

Stores raw listing metadata parsed from CSV input.

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| id | INTEGER | No | AUTOINCREMENT | Primary key |
| title | TEXT | No | | Original title of the GPU listing |
| price | REAL | No | | Price of the GPU |
| canonical_model | TEXT | No | | Canonical model name (e.g., "RTX_A5000") |
| match_type | TEXT | No | | Type of match (exact, regex, fuzzy) |
| match_score | REAL | No | | Confidence score of the match |
| created_at | TIMESTAMP | No | CURRENT_TIMESTAMP | When the record was created |
| updated_at | TIMESTAMP | No | CURRENT_TIMESTAMP | When the record was last updated |
| import_id | TEXT | Yes | | Reference to the import batch |

**Indexes:**
- `idx_listings_canonical_model`: Index on `canonical_model` for faster lookups
- `idx_listings_import_id`: Index on `import_id` for faster lookups

**Foreign Keys:**
- `canonical_model` references `models(model)` with `ON DELETE CASCADE`
- `import_id` references `import_batches(import_id)` with `ON DELETE SET NULL`

### scored_listings

Stores enriched and scored GPU listings.

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| id | INTEGER | No | AUTOINCREMENT | Primary key |
| canonical_model | TEXT | No | | Canonical model name (e.g., "H100_PCIE_80GB") |
| price | REAL | No | | Price in USD |
| vram_gb | INTEGER | No | | VRAM capacity in GB |
| tdp_watts | INTEGER | No | | Thermal Design Power in watts |
| mig_support | INTEGER | Yes | 0 | MIG support level (0-7) |
| nvlink | BOOLEAN | Yes | 0 | NVLink support (0=false, 1=true) |
| generation | TEXT | Yes | | GPU architecture generation |
| cuda_cores | INTEGER | Yes | | Number of CUDA cores |
| slot_width | INTEGER | Yes | | Physical slot width |
| pcie_generation | INTEGER | Yes | | PCIe generation |
| form_factor | TEXT | Yes | "Standard" | Form factor (e.g., "Standard", "SFF") |
| notes | TEXT | Yes | | Additional notes about the GPU |
| warnings | TEXT | Yes | | Warnings about metadata mismatches |
| score | REAL | No | | Calculated utility score |
| condition | TEXT | Yes | | Condition of the GPU (e.g., "new", "used") |
| quantity | INTEGER | Yes | | Available quantity |
| min_order_qty | INTEGER | Yes | | Minimum order quantity |
| seller | TEXT | Yes | | Seller name |
| region | TEXT | Yes | | Region (e.g., "US", "EU") |
| source_url | TEXT | Yes | | Source URL of the listing |
| source_type | TEXT | Yes | | Source type (e.g., "marketplace", "retailer") |
| seen_at | TIMESTAMP | Yes | | When the listing was seen |
| created_at | TIMESTAMP | No | CURRENT_TIMESTAMP | When the record was created |
| updated_at | TIMESTAMP | No | CURRENT_TIMESTAMP | When the record was last updated |
| import_id | TEXT | Yes | | Reference to the import batch |

**Indexes:**
- `idx_scored_listings_canonical_model`: Index on `canonical_model` for faster lookups
- `idx_scored_listings_score`: Index on `score` for faster lookups
- `idx_scored_listings_region`: Index on `region` for faster lookups
- `idx_scored_listings_seen_at`: Index on `seen_at` for faster lookups
- `idx_scored_listings_import_id`: Index on `import_id` for faster lookups

**Foreign Keys:**
- `canonical_model` references `models(model)` with `ON DELETE CASCADE`
- `import_id` references `import_batches(import_id)` with `ON DELETE SET NULL`

### quantized_listings

Stores quantization capacities for GPU listings.

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| id | INTEGER | No | AUTOINCREMENT | Primary key |
| scored_listing_id | INTEGER | No | | Reference to the scored listing |
| model_7b | INTEGER | No | | Number of 7B parameter models that can fit |
| model_13b | INTEGER | No | | Number of 13B parameter models that can fit |
| model_70b | INTEGER | No | | Number of 70B parameter models that can fit |
| created_at | TIMESTAMP | No | CURRENT_TIMESTAMP | When the record was created |
| updated_at | TIMESTAMP | No | CURRENT_TIMESTAMP | When the record was last updated |
| import_id | TEXT | Yes | | Reference to the import batch |

**Indexes:**
- `idx_quantized_listings_scored_listing_id`: Index on `scored_listing_id` for faster lookups

**Foreign Keys:**
- `scored_listing_id` references `scored_listings(id)` with `ON DELETE CASCADE`
- `import_id` references `import_batches(import_id)` with `ON DELETE SET NULL`

## Triggers

The schema includes triggers to automatically update the `updated_at` timestamp when records are modified:

- `update_models_timestamp`: Updates `models.updated_at` when a record is modified
- `update_listings_timestamp`: Updates `listings.updated_at` when a record is modified
- `update_scored_listings_timestamp`: Updates `scored_listings.updated_at` when a record is modified
- `update_quantized_listings_timestamp`: Updates `quantized_listings.updated_at` when a record is modified

## Relationships

The schema includes the following relationships:

- `import_batches` has many `models`, `listings`, `scored_listings`, and `quantized_listings`
- `models` has many `listings` and `scored_listings`
- `scored_listings` has one `quantized_listing`

## Usage

### Instantiating the Schema

The schema can be instantiated using the following command:

```bash
uv run -m glyphd init-db --db-path data/gpu.db
```

### Migrations

Migrations are managed using Alembic. The initial migration creates all tables, indexes, and triggers.

Future migrations will be added as needed to support schema evolution.

## Design Considerations

### Extensibility

The schema is designed to be extensible:

- New fields can be added to existing tables without breaking existing code
- New tables can be added to support new features
- The `schema_version` table tracks schema changes

### Query Performance

The schema includes indexes on fields that are likely to be used in queries:

- `models.model`: For looking up models by name
- `listings.canonical_model`: For looking up listings by model
- `scored_listings.canonical_model`: For looking up scored listings by model
- `scored_listings.score`: For filtering by score
- `scored_listings.region`: For filtering by region
- `scored_listings.seen_at`: For filtering by date

### Import Versioning

The schema supports import versioning through the `import_batches` table:

- Each import batch has a unique `import_id`
- Records can be associated with an import batch via the `import_id` field
- This enables differential updates and tracking of data provenance