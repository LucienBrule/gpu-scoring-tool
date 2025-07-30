from abc import ABC, abstractmethod
from importlib.resources import files
from typing import Type

from .base_resource_loader import ResourceLoader, T


class BaseSqlLoader(ResourceLoader, ABC):
    @property
    @abstractmethod
    def resource_uri(self) -> str:
        """The importable module path to the resource directory."""
        ...

    def load(self, model: Type[T], resource_name: str) -> T:
        """Load a resource and return it parsed into the given Pydantic model."""
        # This method is required by ResourceLoader interface but not used for SQL files
        raise NotImplementedError("SQL files should be loaded using load_text() method")

    def load_text(self, resource_name: str) -> str:
        """Load a SQL resource and return it as raw text."""
        resource_path = files(self.resource_uri).joinpath(resource_name)
        return resource_path.read_text(encoding="utf-8")
