from .base_yaml_loader import BaseYamlLoader


class GlyphSieveYamlLoader(BaseYamlLoader):
    @property
    def resource_uri(self) -> str:
        return "glyphsieve.resources"
