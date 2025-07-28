from glyphsieve.core.resources.base_csv_loader import BaseCsvLoader


class GlyphdCSVLoader(BaseCsvLoader):
    @property
    def resource_uri(self) -> str:
        return "glyphd.resources"
