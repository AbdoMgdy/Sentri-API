from app import ma
from .model import Customer
# from app.order.schema import OrderSchema


class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        load_instance = True
    # orders = ma.Nested(OrderSchema, many=True)
