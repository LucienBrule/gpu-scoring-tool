"""
Pickle Loader for GlyphSieve Resources

This module provides a loader for pickle files stored in the glyphsieve resources directory.
"""

import pickle
from importlib.resources import files
from typing import Any


class GlyphSievePklLoader:
    """
    Loader for pickle files from glyphsieve resources.

    This loader follows the same pattern as YamlLoader but is specifically
    designed for loading pickle files (e.g., trained ML models).
    """

    @property
    def resource_uri(self) -> str:
        """The importable module path to the resource directory."""
        return "glyphsieve.resources"

    def load(self, resource_name: str) -> Any:
        """
        Load a pickle file from the glyphsieve resources directory.

        Args:
            resource_name: The name/path of the pickle file relative to the resources directory

        Returns:
            The unpickled object

        Raises:
            FileNotFoundError: If the resource file doesn't exist
            pickle.PickleError: If the file cannot be unpickled
        """
        resource_path = files(self.resource_uri).joinpath(resource_name)

        if not resource_path.is_file():
            raise FileNotFoundError(f"Resource file not found: {resource_name}")

        with resource_path.open("rb") as f:
            return pickle.load(f)
