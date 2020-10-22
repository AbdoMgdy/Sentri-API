from .model import Item


class ItemService():
    @staticmethod
    def get_all(categories):
        items_list = []
        for category in categories:
            temp_items = Item.query.filter_by(category_uuid=category.uuid).all()
            if temp_items:
                items_list.append(temp_items)

        return items_list

    @staticmethod
    def find(uuid):
        return Item.find_by_uuid(uuid)

    @staticmethod
    def create(kwargs):
        new_item = Item(**kwargs)
        return new_item

    @staticmethod
    def remove(uuid):
        print(uuid)
        item = Item.find_by_uuid(uuid)
        item.remove()
        return 'item removed'

    @staticmethod
    def update(uuid, changes):
        item = Item.find_by_uuid(uuid)
        item.update(changes)
        return item
