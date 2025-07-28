import logging
from pathlib import Path
from typing import List, cast

from glyphd.api.models import GPUModelDTO
from glyphd.core.resources.resource_context import GlyphdResourceContext
from glyphsieve.core.resources.yaml_loader import GlyphSieveYamlLoader
from glyphsieve.models.gpu import GPURegistry

logger = logging.getLogger(__name__)


def load_gpu_model_metadata(path: Path) -> List[GPUModelDTO]:
    """
    Load GPU model metadata from a CSV file.

    Args:
        path: Path to the Final_Market_Value_GPU_Summary.csv file

    Returns:
        List of GPUModelDTO objects

    Raises:
        FileNotFoundError: If the file does not exist
        ValidationError: If the data does not match the expected schema
    """
    if not path.exists():
        logger.error(f"GPU model metadata file not found: {path}")
        raise FileNotFoundError(f"File not found: {path}")

    models = cast(List[GPUModelDTO], GlyphdResourceContext().load(GPUModelDTO, path.name))

    # Enrich with specs
    try:
        loader = GlyphSieveYamlLoader()
        gpu_registry = loader.load(GPURegistry, "gpu_specs.yaml")
        specs_by_model = {
            gpu.canonical_model: {
                "vram_gb": gpu.vram_gb,
                "tdp_watts": gpu.tdp_watts,
                "mig_support": gpu.mig_support,
                "nvlink": gpu.nvlink,
                "generation": gpu.generation,
                "cuda_cores": gpu.cuda_cores,
                "slot_width": gpu.slot_width,
                "pcie_generation": gpu.pcie_generation,
            }
            for gpu in gpu_registry.gpus
            if gpu.canonical_model
        }
        for model in models:
            enriched = specs_by_model.get(model.model.replace(" ", "_").upper())
            if enriched:
                for key, value in enriched.items():
                    setattr(model, key, value)
        logger.info(f"Enriched {len(specs_by_model)} models with specs")
    except Exception as e:
        logger.warning(f"Error loading GPU specs: {e}. Will continue with market data only.")

    return models
