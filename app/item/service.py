from .model import Item


class ItemService():
    @staticmethod
    def get_all():
        return Item.query.all()
