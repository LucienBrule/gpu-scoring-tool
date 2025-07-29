"""
Heuristics module for glyphsieve.

This module provides abstract base classes and implementations for heuristic taggers
that can be used to classify GPU listings based on specific criteria.
"""

import math
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional

import pandas as pd

from glyphsieve.core.resources.yaml_loader import GlyphSieveYamlLoader
from glyphsieve.models.heuristic import (
    QuantizationCapacityConfig,
    QuantizationHeuristicConfig,
)
from glyphsieve.models.quantization import QuantizationCapacitySpec


class Heuristic(ABC):
    """
    Abstract base class for heuristic taggers.

    This class defines the interface for heuristic taggers that can be used
    to classify GPU listings based on specific criteria.
    """

    @abstractmethod
    def evaluate(self, row: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate the heuristic for a given row.

        Args:
            row (Dict[str, Any]): The row to evaluate, represented as a dictionary

        Returns:
            Dict[str, Any]: Key-value pairs to be added to the row
        """
        pass


class QuantizationHeuristic(Heuristic):
    """
    Heuristic for quantization capability.

    This heuristic classifies GPUs as quantization-capable based on VRAM, TDP, and MIG support.
    """

    def __init__(self, config: Optional[QuantizationHeuristicConfig] = None):
        """
        Initialize the quantization heuristic.

        Args:
            config (Optional[QuantizationHeuristicConfig]): Configuration for the heuristic.
                If None, loads the default configuration.
        """
        self.config = config or self._load_default_config()

    def _load_default_config(self) -> QuantizationHeuristicConfig:
        """
        Load the default configuration from the YAML file.

        Returns:
            QuantizationHeuristicConfig: The default configuration

        Raises:
            ValueError: If the configuration file is invalid
        """
        try:
            loader = GlyphSieveYamlLoader()
            return loader.load(QuantizationHeuristicConfig, "quantization_heuristic.yaml")
        except FileNotFoundError:
            # If the file doesn't exist, return the default configuration
            return QuantizationHeuristicConfig()
        except Exception as e:
            raise ValueError(f"Invalid configuration file: {e!s}")

    def evaluate(self, row: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate if a GPU is quantization-capable.

        A GPU is considered quantization-capable if it meets all of the following criteria:
        - VRAM >= min_vram_gb
        - TDP <= max_tdp_watts
        - MIG support >= min_mig_support

        Args:
            row (Dict[str, Any]): The row to evaluate, represented as a dictionary

        Returns:
            Dict[str, Any]: A dictionary with the key 'quantization_capable' and a boolean value
        """
        # Check if the required fields are present
        if not all(field in row for field in ["vram_gb", "tdp_watts", "mig_support"]):
            return {"quantization_capable": False}

        # Check if any of the required fields are None
        if any(row[field] is None for field in ["vram_gb", "tdp_watts", "mig_support"]):
            return {"quantization_capable": False}

        # Apply the heuristic criteria
        is_capable = (
            row["vram_gb"] >= self.config.min_vram_gb
            and row["tdp_watts"] <= self.config.max_tdp_watts
            and row["mig_support"] >= self.config.min_mig_support
        )

        return {"quantization_capable": is_capable}


def load_heuristic_config(config_file: Optional[str] = None) -> QuantizationHeuristicConfig:
    """
    Load the quantization heuristic configuration from a YAML file.

    Args:
        config_file (Optional[str]): Path to the YAML file with the configuration.
            If None, uses the default file in the package resources.

    Returns:
        QuantizationHeuristicConfig: The loaded configuration

    Raises:
        ValueError: If the configuration file is invalid
    """
    try:
        loader = GlyphSieveYamlLoader()
        resource_name = config_file or "quantization_heuristic.yaml"
        return loader.load(QuantizationHeuristicConfig, resource_name)
    except FileNotFoundError:
        # If the file doesn't exist, return the default configuration
        return QuantizationHeuristicConfig()
    except Exception as e:
        raise ValueError(f"Invalid configuration file: {e!s}")


class QuantizationCapacityHeuristic(Heuristic):
    """
    Heuristic for quantization capacity calculation.

    This heuristic calculates how many models of different sizes (7B, 13B, 70B) can fit
    on a GPU based on its VRAM.
    """

    def __init__(self, config: Optional[QuantizationCapacityConfig] = None):
        """
        Initialize the quantization capacity heuristic.

        Args:
            config (Optional[QuantizationCapacityConfig]): Configuration for the heuristic.
                If None, loads the default configuration.
        """
        self.config = config or self._load_default_config()

    def _load_default_config(self) -> QuantizationCapacityConfig:
        """
        Load the default configuration from the YAML file.

        Returns:
            QuantizationCapacityConfig: The default configuration

        Raises:
            ValueError: If the configuration file is invalid
        """
        try:
            loader = GlyphSieveYamlLoader()
            return loader.load(QuantizationCapacityConfig, "quantization_heuristic.yaml")
        except FileNotFoundError:
            # If the file doesn't exist, raise an error as we need the model size configurations
            raise ValueError("Quantization heuristic configuration file not found")
        except Exception as e:
            raise ValueError(f"Invalid configuration file: {e!s}")

    def evaluate(self, row: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate the quantization capacity for a GPU.

        The capacity is calculated using the formula:
        capacity = floor((vram_gb - overhead_gb) / model_vram_gb)

        Args:
            row (Dict[str, Any]): The row to evaluate, represented as a dictionary

        Returns:
            Dict[str, Any]: A dictionary with the key 'quantization_capacity' and a QuantizationCapacitySpec value
        """
        # Check if the required field is present
        if "vram_gb" not in row or row["vram_gb"] is None:
            # Return zero capacity for all model sizes if VRAM is not available
            return {"quantization_capacity": QuantizationCapacitySpec(**{"7b": 0, "13b": 0, "70b": 0})}

        vram_gb = row["vram_gb"]
        overhead_gb = self.config.overhead_gb

        # Calculate capacity for each model size
        available_vram = max(0, vram_gb - overhead_gb)

        model_7b_capacity = math.floor(available_vram / self.config.models.b7)
        model_13b_capacity = math.floor(available_vram / self.config.models.b13)
        model_70b_capacity = math.floor(available_vram / self.config.models.b70)

        # Ensure non-negative values
        model_7b_capacity = max(0, model_7b_capacity)
        model_13b_capacity = max(0, model_13b_capacity)
        model_70b_capacity = max(0, model_70b_capacity)

        # Create the capacity specification
        capacity_spec = QuantizationCapacitySpec(
            **{"7b": model_7b_capacity, "13b": model_13b_capacity, "70b": model_70b_capacity}
        )

        return {"quantization_capacity": capacity_spec}


def load_quantization_capacity_config(config_file: Optional[str] = None) -> QuantizationCapacityConfig:
    """
    Load the quantization capacity configuration from a YAML file.

    Args:
        config_file (Optional[str]): Path to the YAML file with the configuration.
            If None, uses the default file in the package resources.

    Returns:
        QuantizationCapacityConfig: The loaded configuration

    Raises:
        ValueError: If the configuration file is invalid
    """
    try:
        loader = GlyphSieveYamlLoader()
        resource_name = config_file or "quantization_heuristic.yaml"
        return loader.load(QuantizationCapacityConfig, resource_name)
    except FileNotFoundError:
        # If the file doesn't exist, raise an error as we need the model size configurations
        raise ValueError("Quantization capacity configuration file not found")
    except Exception as e:
        raise ValueError(f"Invalid configuration file: {e!s}")


def apply_quantization_capacity(
    input_file: str | Path, output_file: str | Path, config_file: Optional[str] = None, force: bool = False
) -> None:
    """
    Apply quantization capacity calculation to a CSV file.

    Args:
        input_file (Union[str, Path]): Path to the input CSV file
        output_file (Union[str, Path]): Path to the output CSV file
        config_file (Optional[str]): Path to the YAML file with the configuration
        force (bool): Whether to force recalculation if quantization capacity already exists

    Raises:
        FileNotFoundError: If the input file does not exist
        ValueError: If quantization capacity already exists and force is False
    """
    # Load the input CSV
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")

    df = pd.read_csv(input_file)

    # Check if quantization capacity already exists
    if "quantization_capacity.7b" in df.columns and not force:
        raise ValueError(
            "Quantization capacity already exists in the input file. " "Use --force-quantize to recalculate."
        )

    # Load the configuration
    config = load_quantization_capacity_config(config_file)

    # Create the heuristic
    heuristic = QuantizationCapacityHeuristic(config)

    # Apply the heuristic to each row
    for idx, row in df.iterrows():
        result = heuristic.evaluate(row.to_dict())
        if "quantization_capacity" in result:
            capacity = result["quantization_capacity"]
            # Store the capacity values in the DataFrame
            df.at[idx, "quantization_capacity.7b"] = capacity.model_7b
            df.at[idx, "quantization_capacity.13b"] = capacity.model_13b
            df.at[idx, "quantization_capacity.70b"] = capacity.model_70b

    # Write the enriched DataFrame to the output file
    os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
    df.to_csv(output_file, index=False)


def apply_heuristics(input_file: str | Path, output_file: str | Path, config_file: Optional[str] = None) -> None:
    """
    Apply heuristics to a CSV file.

    Args:
        input_file (Union[str, Path]): Path to the input CSV file
        output_file (Union[str, Path]): Path to the output CSV file
        config_file (Optional[str]): Path to the YAML file with the configuration

    Raises:
        FileNotFoundError: If the input file does not exist
    """

    # Load the input CSV
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")

    df = pd.read_csv(input_file)

    # Load the configuration
    config = load_heuristic_config(config_file)

    # Create the heuristic
    heuristic = QuantizationHeuristic(config)

    # Apply the heuristic to each row
    for idx, row in df.iterrows():
        result = heuristic.evaluate(row.to_dict())
        for key, value in result.items():
            df.at[idx, key] = value

    # Write the enriched DataFrame to the output file
    os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
    df.to_csv(output_file, index=False)
