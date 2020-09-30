

from app.category.model import Category
from app.item.model import Item


class CategoryService():
    @staticmethod
    def get_all() -> list[Category]:
        return Category.query.all()

    @staticmethod
    def buid_block(category):
        items = Item.find_by_category_id(category.uuid)
        block_elements = category.block['payload']['elements']
        for item in items:
            block_elements.append(item.block)
        category.save()
