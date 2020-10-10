from app.category.model import Category
from app.category.service import CategoryService
from flask import request
from app.vendor.model import Vendor
from flask_restx import Resource, Namespace
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
api = Namespace('category')


@api.route('/<string:uuid>')
class CatalogResource(Resource):
    # @jwt_required
    def get(self, uuid):
        return CategoryService.get(uuid), 200

    @jwt_required
    def post(self):
        data = request.get_json()
        print(data)
        identity = get_jwt_identity()
        print(identity)
        new_category = CategoryService.create(data)
        return new_category, 200

    # @jwt_required
    def put(self, uuid):
        data = request.get_json()
        print(data)
        CategoryService.update(uuid, data['changes'])

    # @jwt_required
    def delete(self, uuid):
        CategoryService.remove(uuid)


@api.route('/all')
class CatalogResourceAll(Resource):
    @jwt_required
    def get(self):
        identity = get_jwt_identity()
        print(identity)
        vendor = Vendor.find_by_uid(identity)
        cateogries = CategoryService.get_all(vendor.page_id)
        return categories, 200
