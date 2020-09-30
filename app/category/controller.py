from app.category.service import CategoryService
from flask.helpers import send_file
from app.category.model import Category
from flask import request
from flask_restx import Resource, Namespace
# from flask_jwt_extended import (
#     jwt_required, create_access_token,
#     get_jwt_identity
# )
api = Namespace('category')


@api.route('/<string:uuid>')
class CatalogResource(Resource):
    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        data = request.get_json()
        print(data)
        changes = data['changes']
        Category.update(changes)
        Category.save()

    def delete(self):
        pass


@api.rout('/all')
class CatalogResourceAll(Resource):
    def get(self):
        CategoryService.get_all()
