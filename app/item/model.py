from sqlalchemy_json import NestedMutableJson
from app import db
from uuid import uuid1


class Item (db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    created_time = db.Column(db.DateTime)
    category_uuid = db.Column(db.String, db.ForeignKey('categories.uuid'), unique=True)
    uuid = db.Column(db.String, unique=True)
    variants = db.Column(NestedMutableJson)
    title = db.Column(db.String)
    subtitle = db.Column(db.String)
    in_stock = db.Column(db.Boolean)
    img_url = db.Column(db.String)
    options = db.Column(NestedMutableJson)
    discount = db.Column(NestedMutableJson)

    def __init__(self, img='', category_uuid='',  title='', in_stock=True, subtitle='', variants=[], options=[], discount={'fixed': True, 'value': 0}):

        self.category_uuid = category_uuid,
        self.uuid = uuid1().hex
        self.variants = variants,
        self.title = title,
        self.subtitle = subtitle,
        self.in_stock = in_stock,
        self.img = img,
        self.options = options,
        self.discount = discount,
        self.block = self.make_item_block()

    # Class Mehtods
    @classmethod
    def find_by_category_uid(cls, category_uuid):
        return cls.query.filter_by(category_uuid=category_uuid).all()

    @classmethod
    def find_by_uuid(cls, uuid):
        return cls.query.filter_by(uuid=uuid).first()

    def add_variant(self, title, price):
        temp = {
            'title': title,
            'price': price
        }
        self.variants[title] = temp

    def set_discount(self, type, value):
        self.discount = {'type': type, 'value': value}

    def make_item_block(self):
        return {
            'title': self.title,
            'image_url': self.img,
            'subtitle': self.subtitle,
            'buttons': [{
                'type': 'web_url',
                'title': f'اطلب بـ{self.price}ج',
                'url': f'https://rest-bot-dev.herokuapp.com/webview/order/{self.uuid}',
                'webview_height_ratio': 'tall',
                'messenger_extensions': 'true'
            }]
        }
# Default Model Methods

    def update(self, changes):
        for key, val in changes.items():
            setattr(self, key, val)
        return self

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.remove(self)
        db.session.commit()
