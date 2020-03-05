from .model import Vendor
from .schema import VendorSchema

BASE_ROUTE = 'vendor'


def register_routes(app, api):
    from .controller import api as vendor_api
    api.add_namespace(vendor_api, path=f'/{BASE_ROUTE}')
