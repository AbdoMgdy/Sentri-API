from flask import jsonify, request
from flask_restx import Resource, Namespace
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity
)
from .model import Catalog
from ..vendor.model import Vendor


api = Namespace('Catalog')


@api.route('/<string:resource>')
class CatalogResource(Resource):
    @jwt_required
    def get(self, resource):
        identity = get_jwt_identity()
        print(identity)
        vendor = Vendor.find_by_uid(identity)
        print(vendor)
        catalog = Catalog.find_by_page_id(vendor.page_id)
        print(catalog)
        if not catalog:
            return 'Catalog Not Found'
        if resource == 'items':
            return jsonify(catalog.items)
        elif resource == 'categories':
            return jsonify(catalog.catgories)

    @jwt_required
    def post(self, resource):
        data = request.get_json()
        print(data)
        identity = get_jwt_identity()
        print(identity)
        vendor = Vendor.find_by_uid(identity)
        print(vendor)
        catalog = Catalog.find_by_page_id(vendor.page_id)
        print(catalog)
        if data['img'] is None:
            data['img'] = ""
        if not catalog:
            return 'Catalog Not Found'
            print('Catalog Not Found')
        if resource == 'items':
            catalog.add_item(data['category'], data['title'],
                             data['subtitle'], data['price'], data['img'], data['in_stock'])
            print('Item Added Successfully')
            return f'{resource} added successfully'
        elif resource == 'categories':
            catalog.add_category(data['title'],
                                 data['subtitle'], data['img'])
            print('Category Added Successfully')
        return f'{resource} added successfully'

    @jwt_required
    def put(self, resource):
        data = request.get_json()
        print(data)
        identity = get_jwt_identity()
        print(identity)
        vendor = Vendor.find_by_uid(identity)
        print(vendor)
        catalog = Catalog.find_by_page_id(vendor.page_id)
        print(catalog)
        if not catalog:
            return 'Catalog Not Found'
            print('Catalog Not Found')
        if resource == 'items':
            catalog.edit_item(data)
            print('Item Edited Successfully')
            return f'{resource} Edited successfully'
        elif resource == 'categories':
            catalog.edit_category(data)
            print('Category Edited Successfully')
        return f'{resource} Edited successfully'

    @jwt_required
    def delete(self, resource):
        data = request.get_json()
        print(data)
        identity = get_jwt_identity()
        print(identity)
        vendor = Vendor.find_by_uid(identity)
        print(vendor)
        catalog = Catalog.find_by_page_id(vendor.page_id)
        print(catalog)
        if not catalog:
            return 'Catalog Not Found'
            print('Catalog Not Found')
        if resource == 'items':
            catalog.remove_item(data['id'])
            print('Item Removed Successfully')
            return f'{resource} Removed successfully'
        elif resource == 'categories':
            catalog.remove_category(data['id'])
            print('Category Removed Successfully')
        return f'{resource} Removed successfully'
