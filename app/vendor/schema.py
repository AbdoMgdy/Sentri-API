from app import ma
from .model import Vendor
from app.order.schema import OrderSchema
from app.customer.schema import CustomerSchema


class VendorSchema(ma.ModelSchema):
    class Meta:
        model = Vendor
    customers = ma.Nested(CustomerSchema)
    orders = ma.Nested(OrderSchema)
