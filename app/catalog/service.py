from ..category import Category


class CatalogService():
    @staticmethod
    def build_main_menu():
        pass

    @staticmethod
    def buid_blocks(catalog):
        categories = Category.find_by_uuid(catalog.uuid)
        block_elements = catalog.block['payload']['elements']
        for category in categories:
            block_elements.append(category.block)
        catalog.save()
