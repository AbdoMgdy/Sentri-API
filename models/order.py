from db import db
import random


class Order(db.Model):
    __tablename__ = 'orders'
    __table_args__ = (db.UniqueConstraint('user', 'number'), )
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    items = db.Column(db.PickleType)
    total = db.Column(db.Float(precision=2))
    is_confirmed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.psid'))
    user = db.relationship('User')

    def __init__(self, user_id):
        self.user_id = user_id
        self.number = random.randint(1000, 99999)
        self.items = []
        self.total = 0
        self.is_confirmed = False

    @classmethod
    def find_by_number(cls, number):
        return cls.query.filter_by(number=number).first()

    def add_item(self, name, quantity, _type, notes, price):
        item = {}
        item['name'] = name
        item['quantity'] = quantity
        item['type'] = _type
        item['notes'] = notes
        item['price'] = price * quantity
        self.items.append(item)
        self.total += item['price']

    def confirm(self):
        self.is_confirmed = True
        db.session.add(self)
        db.session.commit()

    def cancel(self):
        db.session.delete(self)
        db.session.commit()
