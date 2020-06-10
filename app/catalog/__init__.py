from .model import Catalog
from .schema import CatalogSchema

BASE_ROUTE = 'catalog'


def register_routes(app, api):
    from .controller import api as catalog_api
    api.add_namespace(catalog_api, path=f'/{BASE_ROUTE}')
