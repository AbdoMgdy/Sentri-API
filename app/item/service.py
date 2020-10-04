from .model import Item
from ..category import Category


class ItemService():
    @staticmethod
    def get_all():
        return Item.query.all()

    @staticmethod
    def create(kwargs):
        new_item = Item(**kwargs)
        return new_item

    @staticmethod
    def remove(uuid):
        item = Item.find_by_uuid(uuid)
        item.remove()
        return 'item removed'

    @staticmethod
    def update(uuid, changes):
        item = Item.find_by_uuid(uuid)
        item.update(changes)
        return item
