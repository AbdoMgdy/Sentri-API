from app import ma
from .model import Catalog


class CatalogSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Catalog
        load_instance = True
