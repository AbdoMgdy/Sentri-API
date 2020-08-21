from app import ma
from .model import Catalog
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class CatalogSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Catalog
        load_instance = True
