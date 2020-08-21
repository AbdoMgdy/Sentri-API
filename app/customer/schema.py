from app import ma
from .model import Customer
# from app.order.schema import OrderSchema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class CustomerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        load_instance = True
    # orders = ma.Nested(OrderSchema, many=True)
