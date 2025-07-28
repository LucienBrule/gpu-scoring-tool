from abc import ABC, abstractmethod
from typing import Type, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class ResourceLoader(ABC):
    @abstractmethod
    def load(self, model: Type[T], resource_name: str) -> T:
        """Load a resource and return it parsed into the given Pydantic model."""
        pass
