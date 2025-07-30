from glyphd.core.resources.csv_loader import GlyphdCSVLoader
from glyphd.core.resources.sql_loader import GlyphdSqlLoader
from glyphd.core.resources.yaml_loader import GlyphdYamlLoader
from glyphsieve.core.resources.base_resource_context import ResourceContext


class GlyphdResourceContext(ResourceContext):
    def get_loaders(self):
        return {
            ".csv": GlyphdCSVLoader(),
            ".sql": GlyphdSqlLoader(),
            ".yaml": GlyphdYamlLoader(),
            ".yml": GlyphdYamlLoader(),
        }
