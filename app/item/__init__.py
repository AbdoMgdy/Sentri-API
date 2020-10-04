from .model import Item
from .shcema import ItemSchema
from .service import ItemService
BASE_ROUTE = 'item'


def register_routes(app, api):
    from .controller import api as item_api
    api.add_namespace(item_api, path=f'/{BASE_ROUTE}')
