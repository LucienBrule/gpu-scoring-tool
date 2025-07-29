-- GPU Scoring Tool SQLite Schema
-- This schema defines the tables for storing GPU listings, models, scored listings, and quantization data.

-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

-- Schema version tracking
CREATE TABLE IF NOT EXISTS schema_version (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    version TEXT NOT NULL,
    applied_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    description TEXT
);

-- Insert initial schema version
INSERT INTO schema_version (version, description) 
VALUES ('1.0.0', 'Initial schema creation');

-- Import batch tracking for differential updates
CREATE TABLE IF NOT EXISTS import_batches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    import_id TEXT NOT NULL UNIQUE,  -- User-provided ID for the import batch
    imported_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    source TEXT,                     -- Source of the import (e.g., 'csv', 'api')
    record_count INTEGER DEFAULT 0,  -- Number of records in this batch
    description TEXT                 -- Optional description of the import
);

-- GPU Models table (based on GPUModelDTO)
-- Stores normalized GPU model registry with technical specifications
CREATE TABLE IF NOT EXISTS models (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model TEXT NOT NULL UNIQUE,      -- The canonical model name (e.g., 'H100_PCIE_80GB')
    
    -- Technical specifications
    vram_gb INTEGER,                 -- VRAM capacity in GB
    tdp_watts INTEGER,               -- Thermal Design Power in watts
    mig_support INTEGER DEFAULT 0,   -- MIG support level (0-7)
    nvlink BOOLEAN DEFAULT 0,        -- NVLink support (0=false, 1=true)
    generation TEXT,                 -- GPU architecture generation (e.g., 'Hopper', 'Ada')
    cuda_cores INTEGER,              -- Number of CUDA cores
    slot_width INTEGER,              -- Physical slot width
    pcie_generation INTEGER,         -- PCIe generation
    
    -- Market data (aggregated from listings)
    listing_count INTEGER DEFAULT 0, -- Number of listings for this model
    min_price REAL,                  -- Minimum price for this model
    median_price REAL,               -- Median price for this model
    max_price REAL,                  -- Maximum price for this model
    avg_price REAL,                  -- Average price for this model
    
    -- Metadata
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    import_id TEXT,                  -- Reference to the import batch
    
    FOREIGN KEY (import_id) REFERENCES import_batches(import_id) ON DELETE SET NULL
);

-- Create index on model name for faster lookups
CREATE INDEX IF NOT EXISTS idx_models_model ON models(model);

-- Raw Listings table (based on GPUListingDTO from glyphsieve)
-- Stores raw listing metadata parsed from CSV input
CREATE TABLE IF NOT EXISTS listings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,             -- Original title of the GPU listing
    price REAL NOT NULL,             -- Price of the GPU
    canonical_model TEXT NOT NULL,   -- Canonical model name (e.g., 'RTX_A5000')
    match_type TEXT NOT NULL,        -- Type of match (exact, regex, fuzzy)
    match_score REAL NOT NULL,       -- Confidence score of the match
    
    -- Metadata
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    import_id TEXT,                  -- Reference to the import batch
    
    FOREIGN KEY (canonical_model) REFERENCES models(model) ON DELETE CASCADE,
    FOREIGN KEY (import_id) REFERENCES import_batches(import_id) ON DELETE SET NULL
);

-- Create indexes for faster lookups
CREATE INDEX IF NOT EXISTS idx_listings_canonical_model ON listings(canonical_model);
CREATE INDEX IF NOT EXISTS idx_listings_import_id ON listings(import_id);

-- Scored Listings table (based on GPUListingDTO from glyphd and EnrichedGPUListingDTO)
-- Stores enriched and scored GPU listings
CREATE TABLE IF NOT EXISTS scored_listings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Basic listing information
    canonical_model TEXT NOT NULL,   -- Canonical model name (e.g., 'H100_PCIE_80GB')
    price REAL NOT NULL,             -- Price in USD
    
    -- Enriched fields from GPU metadata
    vram_gb INTEGER NOT NULL,        -- VRAM capacity in GB
    tdp_watts INTEGER NOT NULL,      -- Thermal Design Power in watts
    mig_support INTEGER DEFAULT 0,   -- MIG support level (0-7)
    nvlink BOOLEAN DEFAULT 0,        -- NVLink support (0=false, 1=true)
    
    -- Optional enriched fields
    generation TEXT,                 -- GPU architecture generation
    cuda_cores INTEGER,              -- Number of CUDA cores
    slot_width INTEGER,              -- Physical slot width
    pcie_generation INTEGER,         -- PCIe generation
    
    -- Additional fields from EnrichedGPUListingDTO
    form_factor TEXT DEFAULT 'Standard', -- Form factor (e.g., 'Standard', 'SFF')
    notes TEXT,                      -- Additional notes about the GPU
    warnings TEXT,                   -- Warnings about metadata mismatches
    
    -- Scoring information
    score REAL NOT NULL,             -- Calculated utility score
    
    -- Additional fields from EPIC.persist.sqlite-store requirements
    condition TEXT,                  -- Condition of the GPU (e.g., 'new', 'used')
    quantity INTEGER,                -- Available quantity
    min_order_qty INTEGER,           -- Minimum order quantity
    seller TEXT,                     -- Seller name
    region TEXT,                     -- Region (e.g., 'US', 'EU')
    source_url TEXT,                 -- Source URL of the listing
    source_type TEXT,                -- Source type (e.g., 'marketplace', 'retailer')
    seen_at TIMESTAMP,               -- When the listing was seen
    
    -- Metadata
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    import_id TEXT,                  -- Reference to the import batch
    
    FOREIGN KEY (canonical_model) REFERENCES models(model) ON DELETE CASCADE,
    FOREIGN KEY (import_id) REFERENCES import_batches(import_id) ON DELETE SET NULL
);

-- Create indexes for faster lookups and filtering
CREATE INDEX IF NOT EXISTS idx_scored_listings_canonical_model ON scored_listings(canonical_model);
CREATE INDEX IF NOT EXISTS idx_scored_listings_score ON scored_listings(score);
CREATE INDEX IF NOT EXISTS idx_scored_listings_region ON scored_listings(region);
CREATE INDEX IF NOT EXISTS idx_scored_listings_seen_at ON scored_listings(seen_at);
CREATE INDEX IF NOT EXISTS idx_scored_listings_import_id ON scored_listings(import_id);

-- Quantized Listings table (based on QuantizationCapacitySpec)
-- Stores quantization capacities for GPU listings
CREATE TABLE IF NOT EXISTS quantized_listings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scored_listing_id INTEGER NOT NULL, -- Reference to the scored listing
    model_7b INTEGER NOT NULL,       -- Number of 7B parameter models that can fit
    model_13b INTEGER NOT NULL,      -- Number of 13B parameter models that can fit
    model_70b INTEGER NOT NULL,      -- Number of 70B parameter models that can fit
    
    -- Metadata
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    import_id TEXT,                  -- Reference to the import batch
    
    FOREIGN KEY (scored_listing_id) REFERENCES scored_listings(id) ON DELETE CASCADE,
    FOREIGN KEY (import_id) REFERENCES import_batches(import_id) ON DELETE SET NULL
);

-- Create index for faster lookups
CREATE INDEX IF NOT EXISTS idx_quantized_listings_scored_listing_id ON quantized_listings(scored_listing_id);

-- Triggers to update the updated_at timestamp when records are modified

-- Update models.updated_at when a record is modified
CREATE TRIGGER IF NOT EXISTS update_models_timestamp
AFTER UPDATE ON models
BEGIN
    UPDATE models SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Update listings.updated_at when a record is modified
CREATE TRIGGER IF NOT EXISTS update_listings_timestamp
AFTER UPDATE ON listings
BEGIN
    UPDATE listings SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Update scored_listings.updated_at when a record is modified
CREATE TRIGGER IF NOT EXISTS update_scored_listings_timestamp
AFTER UPDATE ON scored_listings
BEGIN
    UPDATE scored_listings SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Update quantized_listings.updated_at when a record is modified
CREATE TRIGGER IF NOT EXISTS update_quantized_listings_timestamp
AFTER UPDATE ON quantized_listings
BEGIN
    UPDATE quantized_listings SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;