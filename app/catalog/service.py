from app.catalog.model import Catalog
from ..category import Category


class CatalogService():
    @staticmethod
    def build_main_menu():
        pass

    @staticmethod
    def find(page_id):
        catalog = Catalog.find_by_page_id(page_id)
        if catalog:
            return catalog
        return False

    @staticmethod
    def create(page_id):
        new_catalog = Catalog(page_id)
        return new_catalog

    @staticmethod
    def buid_blocks(catalog):
        categories = Category.find_by_uuid(catalog.uuid)
        block_elements = catalog.block['payload']['elements']
        for category in categories:
            block_elements.append(category.block)
        catalog.save()
