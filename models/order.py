from db import db
import random


class Order(db.Model):
    __tablename__='new_orders'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    items = db.Column(db.PickleType)
    price = db.Column(db.Float(precision=2))

    def __init__(self, user_id):
        self.number = random.randint(1000, 99999)
        self.items = []
        self.total = 0
        self.is_done = False
    @classmethod
    def find_by_number(cls, number):
         return cls.query.filter_by(number=number).first()

    def add_item(self, name, quantity, price):
        item = {}
        item['name'] = name
        item['quantity'] = quantity
        item['price'] = price * quantity
        self.items.append(item)
        self.total += item['price']

    def confirm(self):
        self.is_done = True
        db.session.add(self)
        db.session.commit()

    def cancel(self):
        db.session.delete(self)
        db.session.commit()
