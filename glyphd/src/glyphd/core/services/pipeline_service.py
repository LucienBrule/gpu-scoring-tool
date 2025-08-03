"""
Pipeline service for processing raw CSV data through glyphsieve normalization.
"""

import asyncio
import csv
import logging
import tempfile
from pathlib import Path
from typing import List

from glyphd.api.models import GPUListingDTO

logger = logging.getLogger(__name__)


class PipelineService:
    """
    Service for processing raw CSV data through the glyphsieve normalization pipeline.
    
    This service bridges the gap between raw CSV uploads and the glyphsieve pipeline,
    enabling automatic normalization and scoring of GPU listing data.
    """
    
    def __init__(self):
        """Initialize the pipeline service."""
        self._validate_glyphsieve_availability()
    
    def _validate_glyphsieve_availability(self) -> None:
        """
        Validate that glyphsieve modules are available for import.
        
        Raises:
            ImportError: If glyphsieve modules cannot be imported
        """
        try:
            # Test import of key glyphsieve modules
            import glyphsieve.core.normalization
            import glyphsieve.core.scoring  # noqa: F401
            logger.info("Glyphsieve modules successfully imported")
        except ImportError as e:
            logger.error(f"Failed to import glyphsieve modules: {e}")
            raise ImportError(
                "Glyphsieve modules not available. Ensure glyphsieve is installed and accessible."
            ) from e
    
    async def process_raw_csv(
        self,
        csv_data: str,
        import_id: str,
        background: bool = False
    ) -> List[GPUListingDTO]:
        """
        Process raw CSV data through the glyphsieve normalization pipeline.
        
        Args:
            csv_data: Raw CSV content as string
            import_id: Unique identifier for this import batch
            background: Whether to process in background (not implemented yet)
            
        Returns:
            List of processed GPUListingDTO objects
            
        Raises:
            ValueError: If CSV data is malformed or processing fails
            RuntimeError: If pipeline processing encounters errors
        """
        if background:
            # For now, process synchronously - background processing can be added later
            logger.warning("Background processing not yet implemented, processing synchronously")
        
        logger.info(f"Starting pipeline processing for import_id: {import_id}")
        
        try:
            # Process the CSV data through the pipeline
            processed_listings = await self._process_csv_sync(csv_data, import_id)
            
            logger.info(
                f"Successfully processed {len(processed_listings)} listings for import_id: {import_id}"
            )
            
            return processed_listings
            
        except Exception as e:
            logger.error(f"Pipeline processing failed for import_id {import_id}: {e}")
            raise RuntimeError(f"Pipeline processing failed: {e}") from e
    
    async def _process_csv_sync(self, csv_data: str, import_id: str) -> List[GPUListingDTO]:
        """
        Process CSV data synchronously through the glyphsieve pipeline.
        
        Args:
            csv_data: Raw CSV content
            import_id: Import batch identifier
            
        Returns:
            List of processed GPUListingDTO objects
        """
        # Create temporary file for processing
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
            temp_file.write(csv_data)
            temp_path = Path(temp_file.name)
        
        try:
            # Process the temporary file through glyphsieve pipeline
            processed_listings = await self._run_glyphsieve_pipeline(temp_path, import_id)
            return processed_listings
            
        finally:
            # Clean up temporary file
            if temp_path.exists():
                temp_path.unlink()
    
    async def _run_glyphsieve_pipeline(self, csv_path: Path, import_id: str) -> List[GPUListingDTO]:
        """
        Run the glyphsieve pipeline on a CSV file.
        
        Args:
            csv_path: Path to the CSV file to process
            import_id: Import batch identifier
            
        Returns:
            List of processed GPUListingDTO objects
        """
        try:
            # Import glyphsieve modules
            from glyphsieve.core.enrichment import enrich_csv
            from glyphsieve.core.normalization import normalize_csv
            from glyphsieve.core.scoring import score_csv
            
            # Create temporary files for pipeline stages
            with tempfile.NamedTemporaryFile(mode='w', suffix='_normalized.csv', delete=False) as norm_file:
                normalized_path = Path(norm_file.name)
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='_enriched.csv', delete=False) as enrich_file:
                enriched_path = Path(enrich_file.name)
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='_scored.csv', delete=False) as score_file:
                scored_path = Path(score_file.name)
            
            try:
                # Step 1: Run normalization: raw CSV -> normalized CSV
                logger.info(f"Step 1: Normalizing CSV file: {csv_path}")
                await asyncio.to_thread(
                    normalize_csv,
                    str(csv_path),
                    str(normalized_path),
                    fuzzy_threshold=80.0,
                    use_ml=False
                )
                
                # Debug: Check normalized CSV columns
                import pandas as pd
                norm_df = pd.read_csv(normalized_path)
                logger.info(f"Normalized CSV columns: {list(norm_df.columns)}")
                logger.info(f"Normalized CSV shape: {norm_df.shape}")
                
                # Step 2: Run enrichment: normalized CSV -> enriched CSV
                logger.info(f"Step 2: Enriching normalized CSV file: {normalized_path}")
                await asyncio.to_thread(
                    enrich_csv,
                    str(normalized_path),
                    str(enriched_path)
                )
                
                # Debug: Check enriched CSV columns
                enrich_df = pd.read_csv(enriched_path)
                logger.info(f"Enriched CSV columns: {list(enrich_df.columns)}")
                logger.info(f"Enriched CSV shape: {enrich_df.shape}")
                
                # Step 3: Run scoring: enriched CSV -> scored CSV
                logger.info(f"Step 3: Scoring enriched CSV file: {enriched_path}")
                await asyncio.to_thread(
                    score_csv,
                    str(enriched_path),
                    str(scored_path)
                )
                
                # Debug: Check scored CSV columns
                scored_df = pd.read_csv(scored_path)
                logger.info(f"Scored CSV columns: {list(scored_df.columns)}")
                logger.info(f"Scored CSV shape: {scored_df.shape}")
                
                # Parse and merge enriched + scored data to create GPUListingDTO objects
                gpu_listings = self._merge_enriched_and_scored_data(enriched_path, scored_path, import_id)
                
                logger.info(f"Successfully processed {len(gpu_listings)} listings")
                return gpu_listings
                
            finally:
                # Clean up temporary files
                for temp_path in [normalized_path, enriched_path, scored_path]:
                    if temp_path.exists():
                        temp_path.unlink()
            
        except ImportError as e:
            raise RuntimeError(f"Failed to import glyphsieve modules: {e}") from e
        except Exception as e:
            raise RuntimeError(f"Pipeline processing failed: {e}") from e
    
    def _parse_raw_csv(self, csv_path: Path) -> List[dict]:
        """
        Parse raw CSV file into list of dictionaries.
        
        Args:
            csv_path: Path to the CSV file
            
        Returns:
            List of dictionaries representing CSV rows
            
        Raises:
            ValueError: If CSV is malformed or empty
        """
        try:
            with open(csv_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                if not reader.fieldnames:
                    raise ValueError("CSV file has no header row")
                
                listings = []
                for row_num, row in enumerate(reader, start=1):
                    # Basic validation - check if row has any non-empty values
                    if any(value.strip() for value in row.values() if value):
                        listings.append(row)
                    else:
                        logger.warning(f"Skipping empty row {row_num} in CSV")
                
                if not listings:
                    raise ValueError("CSV file contains no valid data rows")
                
                return listings
                
        except FileNotFoundError:
            raise ValueError(f"CSV file not found: {csv_path}")
        except csv.Error as e:
            raise ValueError(f"Malformed CSV file: {e}")
        except Exception as e:
            raise ValueError(f"Error parsing CSV file: {e}")
    
    
    def _merge_enriched_and_scored_data(self, enriched_path: Path, scored_path: Path, import_id: str) -> List[GPUListingDTO]:
        """
        Merge enriched CSV data with scored CSV data to create GPUListingDTO objects.
        
        Args:
            enriched_path: Path to the enriched CSV file
            scored_path: Path to the scored CSV file
            import_id: Import batch identifier
            
        Returns:
            List of GPUListingDTO objects
            
        Raises:
            ValueError: If CSV files are malformed or missing required fields
        """
        try:
            import pandas as pd
            
            # Load both CSV files
            enriched_df = pd.read_csv(enriched_path)
            scored_df = pd.read_csv(scored_path)
            
            if len(enriched_df) != len(scored_df):
                raise ValueError(f"Row count mismatch: enriched={len(enriched_df)}, scored={len(scored_df)}")
            
            gpu_listings = []
            
            for index in range(len(enriched_df)):
                enriched_row = enriched_df.iloc[index]
                scored_row = scored_df.iloc[index]
                
                try:
                    # Map enriched field names to GPUListingDTO field names
                    gpu_listing = GPUListingDTO(
                        canonical_model=enriched_row['canonical_model'],
                        vram_gb=int(float(enriched_row['vram_gb'])) if pd.notna(enriched_row['vram_gb']) else 0,
                        mig_support=int(float(enriched_row['mig_capable'])) if pd.notna(enriched_row['mig_capable']) else 0,
                        nvlink=self._parse_boolean(enriched_row['nvlink']) if pd.notna(enriched_row['nvlink']) else False,
                        tdp_watts=int(float(enriched_row['tdp_w'])) if pd.notna(enriched_row['tdp_w']) else 0,
                        price=float(enriched_row['price']),
                        score=float(scored_row['final_score']) if pd.notna(scored_row['final_score']) else 0.0,
                        import_id=import_id,
                        import_index=index,
                    )
                    gpu_listings.append(gpu_listing)
                    
                except (ValueError, KeyError) as e:
                    logger.warning(f"Skipping invalid row {index} in merged data: {e}")
                    continue
            
            if not gpu_listings:
                raise ValueError("No valid listings found in merged data")
            
            return gpu_listings
            
        except FileNotFoundError as e:
            raise ValueError(f"CSV file not found: {e}")
        except Exception as e:
            raise ValueError(f"Error merging enriched and scored data: {e}")

    def _parse_boolean(self, value: str) -> bool:
        """
        Parse string value to boolean.
        
        Args:
            value: String value to parse
            
        Returns:
            Boolean value
        """
        if isinstance(value, bool):
            return value
        
        if isinstance(value, str):
            return value.lower() in ('true', '1', 'yes', 'on')
        
        return bool(value)