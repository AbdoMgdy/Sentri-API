from app.item.service import ItemService
from app .vendor import Vendor
from app.catalog.service import CatalogService
from app.category.service import CategoryService
from app.category.shcema import CategorySchema
from flask import request
from flask_restx import Resource, Namespace
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
api = Namespace('item')


@api.route('/', '/<string:uuid>')
class ItemResource(Resource):
    def get(self, uuid):
        return ItemService.find(uuid)

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
        print(uuid)
        ItemService.remove(uuid)
        return 'Item Deleted', 200


@api.route('/all')
class ItemResourceAll(Resource):
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
