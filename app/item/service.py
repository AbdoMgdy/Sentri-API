from .model import Item


class ItemService():
    @staticmethod
    def get_all():
        return Item.query.all()

    @staticmethod
    def find(uuid):
        return Item.find_by_uuid(uuid)

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
