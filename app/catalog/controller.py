from flask import jsonify, request
from flask_restx import Resource, Namespace, reqparse

from .model import Catalog


api = Namespace('Catalog')


@api.route('/<string:page_id>/<string:resource>')
class CatalogResource(Resource):
    def get(self, page_id, resource):
        catalog = Catalog.find_by_page_id(page_id)
        if not catalog:
            return 'Catalog Not Found'
        if resource == 'items':
            return catalog.items
        elif resource == 'categories':
            return catalog.categories

    def post(self, page_id, resource):
        data = request.get_json()
        catalog = Catalog.find_by_page_id(page_id)
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
