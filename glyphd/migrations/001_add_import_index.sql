-- Migration: Add import_index column to models and scored_listings tables
-- Version: 1.1.0
-- Description: Add import_index field to align database schema with GPUListingDTO model

-- Add import_index column to models table
ALTER TABLE models ADD COLUMN import_index INTEGER;

-- Add import_index column to scored_listings table
ALTER TABLE scored_listings ADD COLUMN import_index INTEGER;

-- Create indexes for performance on import_id and import_index combination
CREATE INDEX IF NOT EXISTS idx_models_import_batch 
ON models(import_id, import_index);

CREATE INDEX IF NOT EXISTS idx_scored_listings_import_batch 
ON scored_listings(import_id, import_index);

-- Update schema_version table to track this migration
INSERT INTO schema_version (version, description, applied_at) 
VALUES ('1.1.0', 'Add import_index to models and scored_listings tables', CURRENT_TIMESTAMP);

-- Note: Existing records will have NULL import_index values
-- This is acceptable as new imports will populate the field correctly