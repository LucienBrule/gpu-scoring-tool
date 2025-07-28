import csv
from abc import ABC, abstractmethod
from importlib.resources import files
from typing import List, Type

from .base_resource_loader import ResourceLoader, T


class BaseCsvLoader(ResourceLoader, ABC):
    @property
    @abstractmethod
    def resource_uri(self) -> str:
        """The importable module path to the resource directory."""
        ...

    def load(self, model: Type[T], resource_name: str) -> List[T]:
        resource_path = files(self.resource_uri).joinpath(resource_name)
        with resource_path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return [model.model_validate(row) for row in reader]
