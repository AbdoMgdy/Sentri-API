

from app.catalog.model import Catalog
from app.catalog.service import CatalogService
from app.category.model import Category
from app.item.model import Item


class CategoryService():
    @staticmethod
    def get_all(catalog_uuid):
        return Category.query.filter_by(catalog_uuid=catalog_uuid).all()

    @staticmethod
    def find(uuid):
        return Category.find_by_uuid(uuid)

    @staticmethod
    def create(kwargs, catalog_uuid):
        catalog = CatalogService.find(catalog_uuid)
        if not catalog:
            catlaog = CatalogService.create(catalog_uuid)
        category = Category(catalog.uuid, **kwargs)
        category.save()
        return category

    @staticmethod
    def update(uuid, changes):
        category = Category.find_by_uuid(uuid)
        category.update(changes)
        category.save()
        return category

    @staticmethod
    def remove(uuid):
        print(uuid)
        category = Category.find_by_uuid(uuid)
        category.remove()

    @staticmethod
    def buid_blocks(category):
        items = Item.find_by_category_id(category.uuid)
        block_elements = category.block['payload']['elements']
        for item in items:
            block_elements.append(item.block)
        category.save()
        catalog = Catalog.find_by_page_id(category.page_id)
        CatalogService.buid_blocks(catalog)
