from .base_csv_loader import BaseCsvLoader


class GlyphSieveCsvLoader(BaseCsvLoader):
    @property
    def resource_uri(self) -> str:
        return "glyphsieve.resources"
