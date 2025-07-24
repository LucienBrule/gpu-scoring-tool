"""
Heuristics module for glyphsieve.

This module provides abstract base classes and implementations for heuristic taggers
that can be used to classify GPU listings based on specific criteria.
"""
import os
import yaml
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union
from pathlib import Path

from pydantic import BaseModel, Field


class HeuristicConfig(BaseModel):
    """
    Base class for heuristic configuration.
    
    This class should be extended by specific heuristic configurations.
    """
    pass


class QuantizationHeuristicConfig(HeuristicConfig):
    """
    Configuration for the quantization capability heuristic.
    
    This model defines the thresholds for classifying a GPU as quantization-capable.
    """
    min_vram_gb: int = Field(24, description="Minimum VRAM capacity in GB")
    max_tdp_watts: int = Field(300, description="Maximum Thermal Design Power in watts")
    min_mig_support: int = Field(1, description="Minimum MIG support level (0=none, 1-7=supported)")
    
    class Config:
        """Pydantic model configuration."""
        schema_extra = {
            "example": {
                "min_vram_gb": 24,
                "max_tdp_watts": 300,
                "min_mig_support": 1
            }
        }


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
            FileNotFoundError: If the configuration file does not exist
            ValueError: If the configuration file is invalid
        """
        config_file = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "resources",
            "quantization_heuristic.yaml"
        )
        
        if not os.path.exists(config_file):
            # If the file doesn't exist, return the default configuration
            return QuantizationHeuristicConfig()
        
        try:
            with open(config_file, "r") as f:
                config_data = yaml.safe_load(f)
            
            # Validate the data using Pydantic
            return QuantizationHeuristicConfig(**config_data)
        
        except Exception as e:
            raise ValueError(f"Invalid configuration file: {str(e)}")
    
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
            row["vram_gb"] >= self.config.min_vram_gb and
            row["tdp_watts"] <= self.config.max_tdp_watts and
            row["mig_support"] >= self.config.min_mig_support
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
        FileNotFoundError: If the configuration file does not exist
        ValueError: If the configuration file is invalid
    """
    if config_file is None:
        # Use the default configuration file in the package resources
        config_file = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "resources",
            "quantization_heuristic.yaml"
        )
    
    if not os.path.exists(config_file):
        # If the file doesn't exist, return the default configuration
        return QuantizationHeuristicConfig()
    
    try:
        with open(config_file, "r") as f:
            config_data = yaml.safe_load(f)
        
        # Validate the data using Pydantic
        return QuantizationHeuristicConfig(**config_data)
    
    except Exception as e:
        raise ValueError(f"Invalid configuration file: {str(e)}")


def apply_heuristics(
    input_file: Union[str, Path],
    output_file: Union[str, Path],
    config_file: Optional[str] = None
) -> None:
    """
    Apply heuristics to a CSV file.
    
    Args:
        input_file (Union[str, Path]): Path to the input CSV file
        output_file (Union[str, Path]): Path to the output CSV file
        config_file (Optional[str]): Path to the YAML file with the configuration
    
    Raises:
        FileNotFoundError: If the input file does not exist
    """
    import pandas as pd
    
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