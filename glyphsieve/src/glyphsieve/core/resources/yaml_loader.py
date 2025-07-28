from importlib.resources import files
from typing import Type

import yaml

from .base import ResourceLoader, T


class YamlLoader(ResourceLoader):
    def load(self, model: Type[T], resource_name: str) -> T:
        resource_path = files("glyphsieve.resources").joinpath(resource_name)
        with resource_path.open("r") as f:
            data = yaml.safe_load(f)
        return model.parse_obj(data)
