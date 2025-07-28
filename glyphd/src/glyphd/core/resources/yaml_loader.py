from glyphsieve.core.resources.base_yaml_loader import BaseYamlLoader


class GlyphdYamlLoader(BaseYamlLoader):
    @property
    def resource_uri(self) -> str:
        return "glyphd.resources"
