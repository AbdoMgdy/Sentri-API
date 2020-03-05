from .model import Customer
from .schema import CustomerSchema

BASE_ROUTE = 'customer'


def register_routes(app, api):
    from .controller import api as customer_api
    api.add_namespace(customer_api, path=f'/{BASE_ROUTE}')
