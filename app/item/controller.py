import uuid
from app.item.service import ItemService
from app.category.service import CategoryService
from app.category.model import Category
from flask import request
from flask_restx import Resource, Namespace
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
from .model import Item
api = Namespace('item')


@api.route('/<string:uuid>')
class ItemResource(Resource):
    def get(self, uuid):
        return ItemService.find(uuid)

    @jwt_required
    def post(self):
        data = request.get_json()
        print(data)
        new_item = ItemService.create(data)
        return new_item, 200

    def put(self, uuid):
        data = request.get_json()
        print(data)
        updated_item = ItemService.update(uuid, data['changes'])
        category = CategoryService.find(updated_item.category_id)
        CategoryService.buid_blocks(category.block)
        return updated_item, 200

    def delete(self, uuid):
        ItemService.remove(uuid)
        return 'Item Deleted', 200


@api.route('/all')
class ItemResourceAll(Resource):
    def get(self):
        ItemService.get_all()
