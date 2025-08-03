import csv
import logging
from functools import lru_cache
from pathlib import Path
from typing import List

from glyphd.api.models import GPUModelDTO

logger = logging.getLogger(__name__)


@lru_cache
def get_gpu_models() -> List[GPUModelDTO]:
    """
    Load GPU models from the GPU model metadata file.

    Returns:
        List of GPUModelDTO objects
    """
    try:
        # Get the path to the CSV file in the resources directory
        # From glyphd/src/glyphd/core/dependencies/gpu_models.py, go up to glyphd/src/glyphd/ then into resources/
        resources_dir = Path(__file__).parent.parent.parent / "resources"
        csv_file_path = resources_dir / "market_value_gpu_summary.csv"
        
        if not csv_file_path.exists():
            logger.warning(f"GPU model metadata file not found: {csv_file_path}")
            return []
        
        gpu_models = []
        
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                try:
                    # Map CSV field names to GPUModelDTO field names
                    gpu_model = GPUModelDTO(
                        model=row["Model"],
                        listing_count=int(row["Listing_Count"]),
                        min_price=float(row["Min_Price"]),
                        median_price=float(row["Median_Price"]),
                        max_price=float(row["Max_Price"]),
                        avg_price=float(row["Avg_Price"]),
                    )
                    gpu_models.append(gpu_model)
                except (ValueError, KeyError) as e:
                    logger.warning(f"Skipping invalid GPU model row: {row}. Error: {e}")
                    continue
        
        logger.info(f"Successfully loaded {len(gpu_models)} GPU models")
        return gpu_models
        
    except FileNotFoundError:
        logger.warning("GPU model metadata file not found: market_value_gpu_summary.csv")
        return []
    except Exception as e:
        logger.error(f"Error loading GPU model metadata: {e}")
        return []
