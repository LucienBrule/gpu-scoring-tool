"""
Tests for the GPU model registry.

This module contains tests for the GPU model registry functionality.
"""

from unittest.mock import patch

import pytest

from glyphsieve.core.resources.base_resource_context import ResourceContext
from glyphsieve.models.registry import GPUModelRegistry, GPUModelSpec


class MockResourceContext(ResourceContext):
    """Mock resource context for testing."""

    def __init__(self, data=None):
        """Initialize with optional mock data."""
        super().__init__()
        self.data = data

    def get_loaders(self):
        """Return a mapping of file extensions to loader implementations."""
        return {}

    def load(self, model, filename):
        """Mock load method that returns the mock data wrapped in the provided model."""
        if self.data is None:
            raise FileNotFoundError(f"File not found: {filename}")
        
        if model is None:
            return self.data
            
        # If this is a RootModel
        if hasattr(model, '__pydantic_root_model__'):
            # Check if this is the GPUSpecsModel from GPUModelRegistry.load()
            if hasattr(model, 'root') and isinstance(model.root, dict):
                # Create a mock object with a root attribute containing the dictionary
                class MockRootModel:
                    def __init__(self, root):
                        self.root = root
                
                # Create a dictionary of mock GPU spec objects
                if "gpus" in self.data:
                    # Create a list of mock GPU spec objects
                    gpu_specs = []
                    for gpu_data in self.data["gpus"]:
                        # Create a mock GPU spec object
                        class MockGPUSpecModel:
                            def __init__(self, **kwargs):
                                for key, value in kwargs.items():
                                    setattr(self, key, value)
                        
                        gpu_specs.append(MockGPUSpecModel(**gpu_data))
                    
                    # Return a mock object with a root attribute containing the dictionary with gpus key
                    return MockRootModel({"gpus": gpu_specs})
                else:
                    # If there's no gpus key, just return the data as is
                    return MockRootModel(self.data)
            else:
                # For any other RootModel, just return a mock object with the data as the root
                class MockRootModel:
                    def __init__(self, root):
                        self.root = root
                
                return MockRootModel(self.data)
        
        # For other models, just return the data
        return self.data


def test_valid_load():
    """Test loading valid GPU model data."""
    # Create mock data matching the structure of gpu_specs.yaml
    mock_data = {
        "gpus": [
            {
                "canonical_model": "TEST_GPU_1",
                "vram_gb": 24,
                "tdp_watts": 250,
                "slot_width": 2,
                "mig_support": 7,
                "nvlink": True,
                "generation": "Test",
                "cuda_cores": 5000,
                "pcie_generation": 4,
            },
            {
                "canonical_model": "TEST_GPU_2",
                "vram_gb": 16,
                "tdp_watts": 150,
                "slot_width": 1,
                "mig_support": 0,
                "nvlink": False,
                "generation": "Test",
                "cuda_cores": 3000,
                "pcie_generation": 4,
            },
        ]
    }

    # Create mock resource context
    resource_context = MockResourceContext(mock_data)

    # Create registry and load data
    registry = GPUModelRegistry()
    registry.load(resource_context)

    # Verify that the registry contains the expected models
    models = registry.list()
    assert len(models) == 2
    
    # First model
    assert models[0].name == "TEST GPU 1"
    assert models[0].vram_gb == 24
    assert models[0].tdp_w == 250
    assert models[0].slots == 2
    assert models[0].mig_capable is True
    assert models[0].form_factor == "Dual"
    assert models[0].connectivity == "PCIe 4.0"
    assert "Test architecture, 5000 CUDA cores, NVLink support" in models[0].notes
    
    # Second model
    assert models[1].name == "TEST GPU 2"
    assert models[1].vram_gb == 16
    assert models[1].tdp_w == 150
    assert models[1].slots == 1
    assert models[1].mig_capable is False
    assert models[1].form_factor == "Single"
    assert models[1].connectivity == "PCIe 4.0"
    assert "Test architecture, 3000 CUDA cores" in models[1].notes


def test_error_handling():
    """Test error handling when loading invalid data."""
    # Create mock resource context with no data
    resource_context = MockResourceContext()

    # Create registry
    registry = GPUModelRegistry()

    # Verify that loading raises a RuntimeError
    with pytest.raises(RuntimeError):
        registry.load(resource_context)

    # Create mock resource context with invalid data (missing required fields)
    resource_context = MockResourceContext({"gpus": [{"canonical_model": "Invalid GPU"}]})

    # Verify that loading raises a RuntimeError
    with pytest.raises(RuntimeError):
        registry.load(resource_context)
        
    # Create mock resource context with invalid structure (missing gpus key)
    resource_context = MockResourceContext({"invalid_key": []})

    # Verify that loading raises a RuntimeError
    with pytest.raises(RuntimeError):
        registry.load(resource_context)


def test_registry_lookup():
    """Test looking up a GPU model by name."""
    # Create mock data matching the structure of gpu_specs.yaml
    mock_data = {
        "gpus": [
            {
                "canonical_model": "TEST_GPU_1",
                "vram_gb": 24,
                "tdp_watts": 250,
                "slot_width": 2,
                "mig_support": 7,
                "nvlink": True,
                "generation": "Test",
                "cuda_cores": 5000,
                "pcie_generation": 4,
            },
            {
                "canonical_model": "TEST_GPU_2",
                "vram_gb": 16,
                "tdp_watts": 150,
                "slot_width": 1,
                "mig_support": 0,
                "nvlink": False,
                "generation": "Test",
                "cuda_cores": 3000,
                "pcie_generation": 4,
            },
        ]
    }

    # Create mock resource context
    resource_context = MockResourceContext(mock_data)

    # Create registry and load data
    registry = GPUModelRegistry()
    registry.load(resource_context)

    # Verify that lookup returns the expected model
    model = registry.get("TEST GPU 1")
    assert model is not None
    assert model.name == "TEST GPU 1"
    assert model.vram_gb == 24
    assert model.tdp_w == 250
    assert model.slots == 2
    assert model.mig_capable is True
    assert model.form_factor == "Dual"
    assert model.connectivity == "PCIe 4.0"
    assert "Test architecture, 5000 CUDA cores, NVLink support" in model.notes

    # Verify that lookup returns None for a non-existent model
    model = registry.get("Non-existent GPU")
    assert model is None


def test_fuzzy_matching():
    """Test fuzzy matching of GPU model names."""
    # Create mock data matching the structure of gpu_specs.yaml
    mock_data = {
        "gpus": [
            {
                "canonical_model": "RTX_6000_ADA",
                "vram_gb": 48,
                "tdp_watts": 300,
                "slot_width": 2,
                "mig_support": 7,
                "nvlink": True,
                "generation": "Ada",
                "cuda_cores": 18176,
                "pcie_generation": 4,
            },
            {
                "canonical_model": "RTX_A6000",
                "vram_gb": 48,
                "tdp_watts": 300,
                "slot_width": 2,
                "mig_support": 0,
                "nvlink": True,
                "generation": "Ampere",
                "cuda_cores": 10752,
                "pcie_generation": 4,
            },
        ]
    }

    # Create mock resource context
    resource_context = MockResourceContext(mock_data)

    # Create registry and load data
    registry = GPUModelRegistry()
    registry.load(resource_context)

    # Mock the _find_best_fuzzy_match function to return a known result
    with patch("glyphsieve.core.normalization._find_best_fuzzy_match") as mock_fuzzy:
        mock_fuzzy.return_value = ("RTX 6000 ADA", 90.0)

        # Verify that closest_match returns the expected model
        model = registry.closest_match("RTX 6000 ADA")
        assert model is not None
        assert model.name == "RTX 6000 ADA"
        assert model.vram_gb == 48
        assert model.tdp_w == 300
        assert model.slots == 2
        assert model.mig_capable is True
        assert model.form_factor == "Dual"
        assert model.connectivity == "PCIe 4.0"
        assert "Ada architecture, 18176 CUDA cores, NVLink support" in model.notes

        # Verify that _find_best_fuzzy_match was called with the expected arguments
        mock_fuzzy.assert_called_once()
        args, _ = mock_fuzzy.call_args
        assert args[0] == "rtx 6000 ada"
        assert "RTX 6000 ADA" in args[1]
        assert "RTX A6000" in args[1]

    # Test with a low threshold that should not match
    with patch("glyphsieve.core.normalization._find_best_fuzzy_match") as mock_fuzzy:
        mock_fuzzy.return_value = ("RTX 6000 ADA", 60.0)

        # Verify that closest_match returns None
        model = registry.closest_match("RTX 6000 ADA", threshold=70.0)
        assert model is None


def test_form_factor_validation():
    """Test validation of form factor values."""
    # Valid form factors
    valid_form_factors = ["Single", "Dual", "Triple", "Quad", "SFF", "HBM", "SXM"]
    for form_factor in valid_form_factors:
        model = GPUModelSpec(
            name="Test GPU",
            vram_gb=24,
            tdp_w=250,
            slots=2,
            mig_capable=True,
            form_factor=form_factor,
        )
        assert model.form_factor == form_factor

    # Invalid form factor
    with pytest.raises(ValueError):
        GPUModelSpec(
            name="Test GPU",
            vram_gb=24,
            tdp_w=250,
            slots=2,
            mig_capable=True,
            form_factor="Invalid",
        )