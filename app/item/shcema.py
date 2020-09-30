from .model import Item
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class ItemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Item
        load_instance = True
