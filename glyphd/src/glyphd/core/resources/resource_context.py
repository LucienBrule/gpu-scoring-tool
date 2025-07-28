from glyphd.core.resources.csv_loader import GlyphdCSVLoader
from glyphd.core.resources.yaml_loader import GlyphdYamlLoader
from glyphsieve.core.resources.base_resource_context import ResourceContext


class GlyphdResourceContext(ResourceContext):
    def get_loaders(self):
        return {
            ".csv": GlyphdCSVLoader(),
            ".yaml": GlyphdYamlLoader(),
            ".yml": GlyphdYamlLoader(),
        }
