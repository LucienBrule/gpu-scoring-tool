from glyphsieve.core.resources.base_sql_loader import BaseSqlLoader


class GlyphdSqlLoader(BaseSqlLoader):
    @property
    def resource_uri(self) -> str:
        return "glyphd.resources"
