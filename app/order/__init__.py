
from .model import Order
from .schema import OrderSchema

BASE_ROUTE = 'order'


def register_routes(app, api):
    from .controller import api as order_api
    api.add_namespace(order_api, path=f'/{BASE_ROUTE}')
