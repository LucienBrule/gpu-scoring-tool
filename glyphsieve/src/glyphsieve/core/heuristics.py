"""
Heuristics module for glyphsieve.

This module provides abstract base classes and implementations for heuristic taggers
that can be used to classify GPU listings based on specific criteria.
"""

import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional

import pandas as pd

from glyphsieve.core.resources.yaml_loader import YamlLoader
from glyphsieve.models.heuristic import QuantizationHeuristicConfig


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
            loader = YamlLoader()
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
        loader = YamlLoader()
        resource_name = config_file or "quantization_heuristic.yaml"
        return loader.load(QuantizationHeuristicConfig, resource_name)
    except FileNotFoundError:
        # If the file doesn't exist, return the default configuration
        return QuantizationHeuristicConfig()
    except Exception as e:
        raise ValueError(f"Invalid configuration file: {e!s}")


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
