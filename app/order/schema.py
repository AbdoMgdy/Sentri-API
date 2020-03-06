from app import ma
from .model import Order
# from app.vendor.schema import VendorSchema
# from app.customer.schema import CustomerSchema


class OrderSchema(ma.ModelSchema):
    class Meta:
        model = Order
    # customer = ma.Nested(CustomerSchema)
    # vendor = ma.Nested(VendorSchema)
