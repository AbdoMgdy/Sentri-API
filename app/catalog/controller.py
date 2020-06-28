from flask import jsonify, request
from flask_restx import Resource, Namespace
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity
)
from .model import Catalog


api = Namespace('Catalog')


@api.route('/<string:resource>')
class CatalogResource(Resource):
    @jwt_required
    def get(self, resource):
        identity = get_jwt_identity()
        print(identity)
        catalog = Catalog.find_by_page_id(identity)
        if not catalog:
            return 'Catalog Not Found'
        if resource == 'items':
            return catalog.items
        elif resource == 'categories':
            return catalog.categories

    @jwt_required
    def post(self, resource):
        data = request.get_json()
        print(data)
        identity = get_jwt_identity()
        print(identity)
        catalog = Catalog.find_by_page_id(identity)
        if not catalog:
            return 'Catalog Not Found'
        if resource == 'items':
            catalog.add_item(data['category'], data['title'],
                             data['subtitle'], data['price'], data['img'])
        elif resource == 'categories':
            catalog.add_category(data['title'],
                                 data['subtitle'], data['img'])
        return f'{resource} added successfully'

    def put(self):
        pass

    def delete(self):
        pass
