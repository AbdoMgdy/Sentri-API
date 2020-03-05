from app import ma
from .model import Vendor


class VendorSchema(ma.ModelSchema):
    class Meta:
        model = Vendor
