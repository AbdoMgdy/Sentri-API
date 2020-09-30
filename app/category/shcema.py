from .model import Category 
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class CatalogSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        load_instance = True
