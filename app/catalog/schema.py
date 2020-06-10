from app import ma
from .model import Catalog


class CatalogSchema(ma.ModelSchema):
    class Meta:
        model = Catalog
