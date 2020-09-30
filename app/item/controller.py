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


@api.route('/')
class ItemResource(Resource):
    def get(self):
        pass

    @jwt_required
    def post(self):
        data = request.get_json()
        identity = get_jwt_identity()
        new_item = Item()
        new_item.save()
        category = Category.find_by_uuid()
        CategoryService.buid_block(category)
        return 'item Created', 200

    def put(self):
        data = request.get_json()
        print(data)
        changes = data['changes']
        item = Item.find_by_uuid(data['uuid'])
        item.update(changes)
        item.save()
        category = Category.find_by_uuid(item.category_id)
        CategoryService.buid_block(category)
        return 'Item Updated', 200

    def delete(self):
        pass


@api.route('/all')
class ItemResourceAll(Resource):
    def get(self):
        ItemService.get_all()
