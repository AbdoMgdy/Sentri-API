from app import ma
from .model import Vendor
from app.order.schema import OrderSchema
from app.customer.schema import CustomerSchema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class VendorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Vendor
        load_instance = True
    customers = ma.Nested(CustomerSchema, many=True)
    orders = ma.Nested(OrderSchema, many=True)
