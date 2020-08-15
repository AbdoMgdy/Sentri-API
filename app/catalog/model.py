from sqlalchemy_json import NestedMutableJson
import datetime
import json
from ..models.generic import GenericTemplate
from app import db
from uuid import uuid1


class Catalog(db.Model):
    __tablename__ = 'catalogs'

    id = db.Column(db.Integer, primary_key=True)
    created_time = db.Column(db.DateTime)
    page_id = db.Column(db.String, db.ForeignKey(
        'vendors.page_id', ondelete='SET NULL', onupdate="CASCADE"), unique=True, nullable=True)
    blocks = db.Column(NestedMutableJson)
    categories = db.Column(NestedMutableJson)
    knowledge = db.Column(NestedMutableJson)
    items = db.Column(NestedMutableJson)

    def __init__(self, page_id):
        self.page_id = page_id
        self.items = {}
        self.categories = {}
        self.knowledge = {
            'greetings': {
                'label': 'Greetings',
                'values': [
                    {
                        'key': 'welcome',
                        'value': ''
                    },
                    {
                        'key': 'thank you',
                        'value': ''
                    }
                ]
            },
            'comments': {
                'label': 'Comments',
                'values': [
                    {'key': 'Ask_For_Menu',
                     'value': ''},
                    {'key': 'Ask_For_Address',
                     'value': ''},

                ]
            }
        }
        self.blocks = {
            'main_menu': {
                'payload': {
                    'template_type': 'generic',
                    'elements': []
                }
            },
            'get_started': {
                'payload': {
                    'template_type': 'generic',
                    'elements': [
                        {
                            'title': """مرحبا بك في مطعمي
                     انا مساعدك الافتراضي كيف أستطيع مساعدتك؟""",
                            'image_url': 'https://scontent-hbe1-1.xx.fbcdn.net/v/t1.0-9/p960x960/80390516_2962955900382554_7936731969642037248_o.jpg?_nc_cat=108&_nc_ohc=68iQXp-Lxn0AX9pBDCk&_nc_ht=scontent-hbe1-1.xx&_nc_tp=6&oh=f886d8238a13919294e79f9bfb70fa0b&oe=5EFDAE46',
                            'subtitle': '',
                            'buttons': [{
                                'type': 'postback',
                                'title': 'المنيو',
                                'payload': 'main_menu'
                            },
                                {
                                'type': 'postback',
                                    'title': 'العنوان/التليفون',
                                    'payload': 'info'
                            }]

                        }
                    ]
                },
                'qucik_replies': [
                    {
                        'content_type': 'text',
                        'title': 'ابدأ أوردر',
                        'payload': 'main_menu',
                    }
                ]
            }
        }
        self.created_time = datetime.datetime.utcnow()

    # Class Methods

    @classmethod
    def find_by_page_id(cls, page_id):
        return cls.query.filter_by(page_id=page_id).first()

    # Categories Methods

    def add_category(self, title, subtitle, img):
        if len(self.blocks['main_menu']['payload']['elements']) == 13:
            print('Categories exceeded max capacity')
            return 'Categories Full'
        _id = uuid1().hex
        temp = {
            'id': _id,
            'title': title,
            'subtitle': subtitle,
            'img': img,
            'block': make_category_block(_id, title, subtitle, img)
        }
        self.blocks[temp['id']] = {
            'payload': {
                'template_type': 'generic',
                'elements': []
            }
        }
        self.categories[_id] = temp
        self.build_main_menu()
        self.save()

    def remove_category(self, _id):
        self.categories.pop(_id, None)
        self.build_main_menu()
        self.save()

    def edit_category(self, category):
        del self.categories[2004]
        del self.blocks[2004]
        if category['id'].isnumeric():
            category['id'] = uuid1().hex
        category['block'] = make_category_block(
            category['id'], category['title'], category['subtitle'], category['img'])
        self.categories[category['id']] = category
        self.save()

    # Items Methods

    def add_item(self, category_id, title, subtitle, price, img, in_stock):
        _id = uuid1().hex
        category = self.categories[category_id]
        temp = {
            'id': _id,
            'category_id': category_id,
            'category_title': category['title'],
            'title': title,
            'subtitle': subtitle,
            'price': price,
            'in_stock': in_stock,
            'img': img,
            'block': make_item_block(category, _id, title, subtitle, price, img)
        }
        self.items[_id] = temp
        self.build_category(category_id)
        self.save()

    def remove_item(self, _id):
        item = self.items[_id]
        self.items.pop(_id, None)
        if item['category_id'] in self.categories:
            self.build_category(item['category_id'])
        self.save()

    def edit_item(self, item):
        if item['id'].isnumeric():
            item['id'] = uuid1().hex
        item['block'] = make_item_block(item['category'],
                                        item['id'], item['title'], item['subtitle'], item['price'], item['img'])
        self.items[item['id']] = item
        self.save()

    # Knowledge Methods

    def edit_knowledge_value(self, category, key, value):
        for v in self.knowledge[category]['values']:
            if v['key'] == key:
                v['value'] = value
        self.save()

    def set_knowledge(self, value):
        self.knowledge = value
        self.save()

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

    # Menu Building Methods
    def build_main_menu(self):
        temp = []
        print(self.categories.items())
        for k, v in self.categories.items():
            if self.blocks[v['id']]['payload']['elements'] is not None:
                print(k)
                print(v)
                if 'block' not in v:
                    v['block'] = make_category_block(
                        v['id'], v['title'], v['subtitle'], v['img'])
                temp.append(
                    v['block'])

        self.blocks['main_menu']['payload']['elements'] = temp

    def build_category(self, _id):
        temp = []
        category = self.categories[_id]
        for k, v in self.items.items():
            print(v)
            if v['category_id'] == _id and v['in_stock']:
                temp.append(
                    v['block'])
        self.blocks[_id]['payload']['elements'] = temp


# Block building functions


def make_item_block(category, _id, title, subtitle, price, img):
    return {
        'title': title,
        'image_url': img,
        'subtitle': subtitle,
        'buttons': [{
            'type': 'web_url',
            'title': f'اطلب بـ{price}ج',
            'url': f'https://rest-bot-dev.herokuapp.com/webview/order/{_id}',
            'webview_height_ratio': 'tall',
            'messenger_extensions': 'true'
        }]
    }


def make_category_block(_id, title, subtitle, img):
    return {
        'title': title,
        'subtitle': subtitle,
        'image_url': img,
        'buttons': [
            {
                "type": "postback",
                "title": "عرض المنيو",
                "payload": _id
            }
        ]
    }
