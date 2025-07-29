"""
GPU model registry schema for metadata integration.

This module defines Pydantic models for GPU model specifications and registry.
"""

import re
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, RootModel, field_validator


class GPUModelSpec(BaseModel):
    """
    Pydantic model for GPU model specifications.

    This model defines the structure of GPU model specifications, including name, VRAM, TDP, slots, etc.
    """

    name: str = Field(..., description="Canonical model name")
    vram_gb: int = Field(..., description="VRAM capacity in GB")
    tdp_w: int = Field(..., description="Thermal Design Power in watts")
    slots: int = Field(..., description="Physical slot width")
    mig_capable: bool = Field(..., description="MIG capability")
    form_factor: str = Field(..., description="Form factor (e.g., Dual, Single)")
    connectivity: Optional[str] = Field(None, description="Connectivity (e.g., PCIe 4.0, NVLink, SXM)")
    notes: Optional[str] = Field(None, description="Additional notes")

    @field_validator("form_factor")
    @classmethod
    def validate_form_factor(cls, v: str) -> str:
        """Validate form factor values."""
        valid_patterns = [
            r"^Single$",
            r"^Dual$",
            r"^Triple$",
            r"^Quad$",
            r"^SFF$",  # Small Form Factor
            r"^HBM$",  # High Bandwidth Memory
            r"^SXM$",  # SXM form factor
        ]

        if not any(re.match(pattern, v) for pattern in valid_patterns):
            raise ValueError(f"Invalid form factor: {v}. Must be one of: Single, Dual, Triple, Quad, SFF, HBM, SXM")
        return v


class GPUModelRegistry:
    """
    Registry of GPU model specifications.

    This class provides methods to load and access GPU model specifications from a YAML file.
    """

    def __init__(self):
        """Initialize the registry."""
        self._models: Dict[str, GPUModelSpec] = {}
        self._loaded = False

    def load(self, resource_context, filename: str = "gpu_specs.yaml") -> None:
        """
        Load GPU model specifications from a YAML file.

        Args:
            resource_context: The resource context to use for loading
            filename: The name of the YAML file to load

        Raises:
            RuntimeError: If the YAML file is missing or malformed
        """
        try:
            # Define models for loading the GPU specs
            class GPUSpecModel(BaseModel):
                canonical_model: str
                vram_gb: int
                tdp_watts: int
                slot_width: int
                mig_support: int
                nvlink: bool
                generation: str
                cuda_cores: int
                pcie_generation: int

            class GPUSpecsModel(RootModel):
                root: Dict[str, List[GPUSpecModel]]

            # Load the data using the model
            specs_data = resource_context.load(GPUSpecsModel, filename)

            # Check if the gpus key is present in the dictionary
            if "gpus" not in specs_data.root:
                raise RuntimeError("Invalid GPU specs data: missing 'gpus' key")

            # Convert GPU specs to GPUModelSpec objects
            models = []

            # Check if the gpus list is empty
            if not specs_data.root["gpus"]:
                raise RuntimeError("Invalid GPU specs data: 'gpus' list is empty")

            for gpu_spec in specs_data.root["gpus"]:
                try:
                    # Check if gpu_spec is a dictionary or an object
                    if isinstance(gpu_spec, dict):
                        # If it's a dictionary, access fields using dictionary syntax
                        canonical_model = gpu_spec["canonical_model"]
                        vram_gb = gpu_spec["vram_gb"]
                        tdp_watts = gpu_spec["tdp_watts"]
                        slot_width = gpu_spec["slot_width"]
                        mig_support = gpu_spec["mig_support"]
                        nvlink = gpu_spec["nvlink"]
                        generation = gpu_spec["generation"]
                        cuda_cores = gpu_spec["cuda_cores"]
                        pcie_generation = gpu_spec["pcie_generation"]
                    else:
                        # If it's an object, access fields using attribute syntax
                        canonical_model = gpu_spec.canonical_model
                        vram_gb = gpu_spec.vram_gb
                        tdp_watts = gpu_spec.tdp_watts
                        slot_width = gpu_spec.slot_width
                        mig_support = gpu_spec.mig_support
                        nvlink = gpu_spec.nvlink
                        generation = gpu_spec.generation
                        cuda_cores = gpu_spec.cuda_cores
                        pcie_generation = gpu_spec.pcie_generation

                    # Map fields from gpu_specs.yaml to GPUModelSpec fields
                    # Convert mig_support (int) to mig_capable (bool)
                    mig_capable = mig_support > 0

                    # Derive form_factor from slot_width
                    form_factor_map = {1: "Single", 2: "Dual", 3: "Triple", 4: "Quad"}
                    form_factor = form_factor_map.get(slot_width, "Dual")

                    # Construct connectivity string from pcie_generation and nvlink
                    connectivity = f"PCIe {pcie_generation}.0"

                    # Create a GPUModelSpec object
                    model = GPUModelSpec(
                        name=canonical_model.replace("_", " "),
                        vram_gb=vram_gb,
                        tdp_w=tdp_watts,
                        slots=slot_width,
                        mig_capable=mig_capable,
                        form_factor=form_factor,
                        connectivity=connectivity,
                        notes=f"{generation} architecture, {cuda_cores} CUDA cores"
                        + (", NVLink support" if nvlink else ""),
                    )
                    models.append(model)
                except KeyError as e:
                    # Re-raise KeyError as RuntimeError for missing required fields
                    raise RuntimeError(f"Missing required field in GPU spec: {e!s}")
                except Exception:
                    # Re-raise any other exceptions
                    raise

            # Convert to dictionary
            self._models = {model.name: model for model in models}
            self._loaded = True
        except Exception as e:
            raise RuntimeError(f"Failed to load GPU model registry: {e!s}")

    def get(self, name: str) -> Optional[GPUModelSpec]:
        """
        Get a GPU model specification by name.

        Args:
            name: The name of the GPU model

        Returns:
            The GPU model specification, or None if not found
        """
        if not self._loaded:
            raise RuntimeError("GPU model registry not loaded. Call load() first.")
        return self._models.get(name)

    def list(self) -> List[GPUModelSpec]:
        """
        List all GPU model specifications.

        Returns:
            A list of all GPU model specifications
        """
        if not self._loaded:
            raise RuntimeError("GPU model registry not loaded. Call load() first.")
        return list(self._models.values())

    def closest_match(self, query: str, threshold: float = 70.0) -> Optional[GPUModelSpec]:
        """
        Find the closest matching GPU model specification.

        Args:
            query: The query string
            threshold: The minimum similarity score (0-100) to consider a match

        Returns:
            The closest matching GPU model specification, or None if no match found
        """
        if not self._loaded:
            raise RuntimeError("GPU model registry not loaded. Call load() first.")

        # Import here to avoid circular imports
        from glyphsieve.core.normalization import _find_best_fuzzy_match

        # Create a dictionary mapping model names to empty lists (no alternatives yet)
        models_dict = {model.name: [] for model in self._models.values()}

        # Find the best fuzzy match
        best_match, best_score = _find_best_fuzzy_match(query.lower(), models_dict)

        # Return the match if above threshold
        if best_score >= threshold and best_match:
            return self._models.get(best_match)

        return None
