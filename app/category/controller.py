from app.category.service import CategoryService
from flask import request
from app.vendor.model import Vendor
from flask_restx import Resource, Namespace
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
api = Namespace('category')


@api.route('/', '/<string:uuid>')
class CategoryResource(Resource):
    # @jwt_required
    def get(self, uuid):
        return CategoryService.get(uuid), 200

    @jwt_required
    def post(self):
        data = request.get_json()
        print(data)
        identity = get_jwt_identity()
        print(identity)
        vendor = Vendor.find_by_uid(identity)
        new_category = CategoryService.create(data, vendor.page_id)
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
class CategoryResourceAll(Resource):
    @jwt_required
    def get(self):
        identity = get_jwt_identity()
        print(identity)
        vendor = Vendor.find_by_uid(identity)
        print(vendor)
        cateogries = CategoryService.get_all(vendor.page_id)
        print(cateogries)
        return categories, 200
