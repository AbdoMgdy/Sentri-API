from app.catalog.service import CatalogService
from app.category.shcema import CategorySchema
from app.category.service import CategoryService
from flask import request, jsonify
from app.vendor.model import Vendor
from flask_restx import Resource, Namespace
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
api = Namespace('category')


@api.route('/', '/<string:uuid>')
class CategoryResource(Resource):
    def get(uuid):
        return CategoryService.get(uuid), 200

    @jwt_required
    def post(self):
        data = request.get_json()
        print(data)
        identity = get_jwt_identity()
        print(identity)
        vendor = Vendor.find_by_uid(identity)
        new_category = CategoryService.create(data, vendor.page_id)
        print(new_category)
        # output = CategorySchema().dump(new_category)
        return 'category_created', 200

    def put(self, uuid):
        data = request.get_json()
        print(data)
        CategoryService.update(uuid, data)
        return 'Category Updated', 201

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
        catalog = CatalogService.find(vendor.page_id)
        cateogries = CategoryService.get_all(catalog.uuid)
        print(cateogries)
        output = CategorySchema().dump(cateogries, many=True)
        print(output)
        return output, 200
