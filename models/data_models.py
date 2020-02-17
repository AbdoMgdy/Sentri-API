
import datetime
import random
import requests

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_json import NestedMutableJson
from flask_login import UserMixin

from models.bot import Bot
from db import db, ma, login


class Vendor(UserMixin, db.Model):
    __tablename__ = 'vendors'
    __table_args__ = (db.UniqueConstraint(
        'page_id', 'id', name='unique_vendor_customers'),)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    username = db.Column(db.String, unique=True)
    menu = db.Column(NestedMutableJson)
    password = db.Column(db.String)
    access_token = db.Column(db.String)
    page_id = db.Column(db.String, unique=True)
    customers = db.relationship('Customer', backref='vendor', lazy='select')

    def __init__(self, name='', user_name='', password='', access_token='', page_id=''):
        self.name = name
        self.username = user_name
        self.password = generate_password_hash(password)
        self.access_token = access_token
        self.page_id = page_id
        self.menu = {}

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def find_by_page_id(cls, page_id):
        return cls.query.filter_by(page_id=page_id).first()

    def save(self):
        print('Vendor_Created')
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.remove(self)
        db.session.commit()


@login.user_loader
def load_user(id):
    return Vendor.query.get(int(id))


class Customer(Bot, db.Model):
    __tablename__ = 'customers'
    __table_args__ = (db.UniqueConstraint(
        'psid', 'id', name='unique_customer_orders'),)
    id = db.Column(db.Integer, primary_key=True)
    psid = db.Column(db.String, unique=True)
    name = db.Column(db.String(80))
    phone_number = db.Column(db.String)
    address = db.Column(db.String)
    # created_time = db.Column(db.DateTime)
    orders = db.relationship('Order', backref='customer', lazy='select')
    page_id = db.Column(db.String, db.ForeignKey('vendors.page_id'))

    def __init__(self, psid, page_id):
        super().__init__()
        self.psid = psid
        self.page_id = page_id
        # self.created_time = datetime.datetime.utcnow()
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
    status = db.Column(db.String)
    time = db.Column(db.DateTime)
    psid = db.Column(db.String, db.ForeignKey('customers.psid'))

    def __init__(self, psid):
        self.psid = psid
        self.time = datetime.datetime.utcnow()
        self.number = random.randint(1000, 99999)
        self.items = []
        self.total = 0
        self.status = 'Pending'

    @classmethod
    def find_by_number(cls, number):
        return cls.query.filter_by(number=number).first()

    @classmethod
    def find_by_customer_id(cls, psid):
        return cls.query.filter_by(user_id=psid).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.get(_id)

    def add_item(self, category='', name='', quantity=0, _type='', notes='', price=0, combo=0):
        item = {}
        item['category'] = category
        item['name'] = name
        item['quantity'] = float(quantity)
        item['type'] = _type
        item['notes'] = notes
        item['combo'] = float(combo)

        item['price'] = float(price)
        # j_item = json.dumps(item)
        self.items.append(item)
        item_price = (float(price) + float(combo)) * float(quantity)
        self.total += item_price
        self.save()

    def edit(self, status):
        self.status = status

    def save(self):
        db.session.add(self)
        db.session.commit()

    def cancel(self):
        db.session.delete(self)
        db.session.commit()


class VendorSchema(ma.ModelSchema):
    class Meta:
        model = Vendor


class CustomerSchema(ma.ModelSchema):
    class Meta:
        model = Customer
    vendor = ma.Nested(VendorSchema)


class OrderSchema(ma.ModelSchema):
    class Meta:
        model = Order
    customer = ma.Nested(CustomerSchema)
