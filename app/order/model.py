from sqlalchemy_json import NestedMutableJson
import string
import datetime
import random
from app import db


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String, unique=True)
    items = db.Column(NestedMutableJson)
    price = db.Column(db.Float(precision=3))
    status = db.Column(db.String)
    is_confirmed = db.Column(db.Boolean)
    time = db.Column(db.DateTime)
    psid = db.Column(db.String, db.ForeignKey('customers.psid'))
    page_id = db.Column(db.String, db.ForeignKey('vendors.page_id'))

    def __init__(self, psid, page_id):
        self.psid = psid
        self.page_id = page_id
        self.time = datetime.datetime.utcnow()
        self.number = ''.join(random.choices(
            string.ascii_lowercase + string.digits, k=6))
        self.items = []
        self.price = 0
        self.is_confirmed = False
        self.status = 'Pending'

    @classmethod
    def find_by_number(cls, number):
        return cls.query.filter_by(number=number).first()

    @classmethod
    def find_by_page_id(cls, page_id):
        return cls.query.filter_by(page_id=page_id).all()

    @classmethod
    def find_by_customer_id(cls, psid):
        return cls.query.filter_by(user_id=psid).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.get(_id)

    def add_item(self, item):
        print(item)
        self.items.append(item)
        self.price += float(item['price']) * float(item['quantity'])
        self.save()

    def update(self, changes):
        for key, val in changes.items():
            setattr(self, key, val)
        self.save()

    def confirm(self):
        self.is_confirmed = True
        self.save()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
