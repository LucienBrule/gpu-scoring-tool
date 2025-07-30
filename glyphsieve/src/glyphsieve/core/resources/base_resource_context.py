from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Type

from pydantic import BaseModel

from glyphsieve.core.resources.base_resource_loader import ResourceLoader


class ResourceContext(ABC):
    def __init__(self):
        self.loaders = self.get_loaders()

    @abstractmethod
    def get_loaders(self) -> dict[str, ResourceLoader]:
        """Return a mapping of file extensions to loader implementations."""
        ...

    def loader_for(self, filename: str) -> ResourceLoader:
        suffix = Path(filename).suffix
        loader = self.loaders.get(suffix)
        if not loader:
            raise ValueError(f"No loader registered for file type: {suffix}")
        return loader

    def load(self, model: Type[BaseModel], filename: str) -> BaseModel | List[BaseModel]:
        return self.loader_for(filename).load(model, filename)

    def load_text(self, filename: str) -> str:
        """Load a resource as raw text (for SQL files, etc.)."""
        loader = self.loader_for(filename)
        if hasattr(loader, "load_text"):
            return loader.load_text(filename)
        else:
            raise ValueError(f"Loader for {filename} does not support text loading")
