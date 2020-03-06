from app import ma
from .model import Customer
# from app.order.schema import OrderSchema


class CustomerSchema(ma.ModelSchema):
    class Meta:
        model = Customer
    # orders = ma.Nested(OrderSchema, many=True)
