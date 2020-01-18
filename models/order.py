from db import db, ma
import json
import random


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True)
    items = db.Column(db.JSON)
    total = db.Column(db.Float(precision=2))
    is_confirmed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.String, db.ForeignKey('users.psid'))

    def __init__(self, user_id):
        self.user_id = user_id
        self.number = random.randint(1000, 99999)
        self.items = []
        self.total = 0
        self.is_confirmed = False

    @classmethod
    def find_by_number(cls, number):
        return cls.query.filter_by(number=number).first()

    @classmethod
    def find_by_user_id(cls, psid):
        return cls.query.filter_by(user_id=psid).first()

    def add_item(self, name, quantity, _type, notes, price):
        item = {}
        item['name'] = name
        item['quantity'] = float(quantity)
        item['type'] = _type
        item['notes'] = notes
        item['price'] = price
        j_item = json.dumps(item)
        self.items.append(j_item)
        self.total += float(item['price'])

    def add(self):
        db.session.add(self)
        db.session.commit()

    def cancel(self):
        db.session.delete(self)
        db.session.commit()

    def confirm(self):
        self.is_confirmed = True


class OrderSchema(ma.ModelSchema):
    class Meta:
        Order
