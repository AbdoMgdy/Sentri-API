from .model import Category
from .shcema import CatalogSchema
from .service import CategoryService

BASE_ROUTE = 'category'


def register_routes(app, api):
    from .controller import api as category_api
    api.add_namespace(category_api, path=f'/{BASE_ROUTE}')
