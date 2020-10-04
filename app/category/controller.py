from app.category.service import CategoryService
from app.category.model import Category
from flask import request
from flask_restx import Resource, Namespace
from flask_jwt_extended import (
    jwt_required,
)
api = Namespace('category')


@api.route('/<string:uuid>')
class CatalogResource(Resource):
    # @jwt_required
    def get(self, uuid):
        return CategoryService.get(uuid), 200

    # @jwt_required
    def post(self):
        data = request.get_json()
        print(data)
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
    # @jwt_required
    def get(self):
        CategoryService.get_all()
