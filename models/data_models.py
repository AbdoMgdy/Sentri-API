from db import db, ma
import datetime
from sqlalchemy_json import NestedMutableJson
import random
import requests
from models.bot import Bot


class User(Bot, db.Model):
    __tablename__ = 'users'
    __table_args__ = (db.UniqueConstraint(
        'psid', 'id', name='unique_user_orders'),)
    id = db.Column(db.Integer, primary_key=True)
    psid = db.Column(db.String, unique=True)
    name = db.Column(db.String(80))
    phone_number = db.Column(db.String)
    address = db.Column(db.String)
    orders = db.relationship('Order', backref='user', lazy='select')

    def __init__(self, psid):
        super().__init__()
        self.psid = psid
        self.name = ''
        self.phone_number = 0
        self.address = ''

    @classmethod
    def find_by_psid(cls, psid):
        return cls.query.filter_by(psid=psid).first()

    def get_info(self):
        request_endpoint = '{}/{}'.format(self.graph_url, self.psid)
        response = requests.get(
            request_endpoint,
            params=self.auth_args
        )
        result = response.json()
        self.name = result['first_name']

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.remove(self)
        db.session.commit()


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True)
    items = db.Column(NestedMutableJson)
    total = db.Column(db.Float(precision=3))
    is_confirmed = db.Column(db.Boolean, default=False)
    time = db.Column(db.DateTime)
    psid = db.Column(db.String, db.ForeignKey('users.psid'))

    def __init__(self, psid):
        self.psid = psid
        self.time = datetime.datetime.utcnow()
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

    def add_item(self, name='', quantity=0, _type='', notes='', price=0, combo=0):
        item = {}
        item['name'] = name
        item['quantity'] = quantity
        item['type'] = _type
        item['notes'] = notes
        item['combo'] = combo

        item['price'] = float(price)
        # j_item = json.dumps(item)
        self.items.append(item)
        if combo != 0:
            combo_price = float(combo) * float(quantity)
        item_price = float(price) * float(quantity)
        self.total += item_price + combo_price
        self.save()

    def edit(self):
        pass

    def save(self):
        db.session.add(self)
        db.session.commit()

    def cancel(self):
        db.session.delete(self)
        db.session.commit()

    def confirm(self):
        self.is_confirmed = True
        self.save()


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User


class OrderSchema(ma.ModelSchema):
    class Meta:
        model = Order
    user = ma.Nested(UserSchema)
