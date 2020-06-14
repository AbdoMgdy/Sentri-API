from sqlalchemy_json import NestedMutableJson
import datetime
from ..models.generic import GenericTemplate
from app import db
from uuid import uuid1


class Catalog(db.Model):
    __tablename__ = 'catalogs'

    id = db.Column(db.Integer, primary_key=True)
    created_time = db.Column(db.DateTime)
    page_id = db.Column(db.String, db.ForeignKey(
        'vendors.page_id'), unique=True)
    blocks = db.Column(NestedMutableJson)
    catgories = db.Column(NestedMutableJson)
    items = db.Column(NestedMutableJson)

    def __init__(self, page_id):
        self.page_id = page_id
        self.items = []
        self.catgories = []
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
                            'title': """مرحبا بك في مطعم سيد حنفي
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

    def add_category(self, title, subtitle, img):
        temp = {
            'id': uuid1().hex,
            'title': title,
            'subtitle': subtitle,
            'img': img,
            'block': self.make_category_block(title, subtitle)
        }
        self.blocks[title] = {
            'payload': {
                'template_type': 'generic',
                'elements': []
            }
        }
        self.blocks['main_menu']['payload']['elements'].append(temp['block'])
        self.catgories.append(temp)
        self.save()

    def remove_category(self, title):
        self.catgories.pop(title, None)
        self.save()

    def edit_category(self):
        pass

    @classmethod
    def find_by_page_id(cls, page_id):
        return cls.query.filter_by(page_id=page_id).first()

    def add_item(self, category, title, subtitle, price, img):
        temp = {
            'id': uuid1().hex,
            'title': title,
            'subtitle': subtitle,
            'price': price,
            'img': img,
            'block': self.make_item_block(category, title, subtitle, price, img)
        }
        self.blocks[category]['payload']['elements'].append(temp['block'])
        self.items.append(temp)
        self.save()

    def make_item_block(category, title, subtitle, price, img):
        return {
            'title': title,
            'image_url': img,
            'subtitle': subtitle,
            'buttons': [{
                'type': 'web_url',
                'title': f'اطلب بـ{price}ج',
                'url': '',
                'webview_height_ratio': 'tall',
                'messenger_extensions': 'true'
            }]
        }

    def make_category_block(title, subtitle):
        return {
            'title': title,
            'subtitle': subtitle,
            'image_url': '',
            'buttons': [
                {
                    "type": "postback",
                    "title": "عرض المنيو",
                    "payload": title
                }
            ]
        }

    def build_menu(self):
        if not self.blocks['main_menu']:
            main_menu = GenericTemplate()
            for k, v in self.catgories.items():
                main_menu.add_element(
                    title=v['title'], image_url=v['img'], subtitle=v['subtitle'], buttons=[{
                        "type": "postback",
                        "title": "عرض المنيو",
                        "payload": v['title']
                    }])
            self.blocks['main_menu'] = main_menu.get_generic()

        for k, v in self.items.items():
            category = GenericTemplate()
            for k, v in self.items[k].items():
                category.add_element(
                    title=v['title'], image_url=v['img'], subtitle=v['subtitle'], buttons=[{
                        "type": "web_url",
                        "title": f"{v['price']}اطلب بـ",
                        "url": ''
                    }])

    def remove_item(self, category, title):
        self.items[category].pop(title, None)
        self.save()

    def edit_item(self):
        pass

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


k = {
    'cat': {
        'item': {

        }
    }

}
