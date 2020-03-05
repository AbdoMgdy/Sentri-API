from app import ma
from .model import Customer


class CustomerSchema(ma.ModelSchema):
    class Meta:
        model = Customer
