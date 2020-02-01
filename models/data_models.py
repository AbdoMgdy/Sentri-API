
import datetime
import random
import requests

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_json import NestedMutableJson
from flask_login import UserMixin

from models.bot import Bot
from db import db, ma, login


class LoginUser(UserMixin, db.Model):
    __tablename__ = 'login_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __init__(self, user_name, password):
        self.username = user_name
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.remove(self)
        db.session.commit()


@login.user_loader
def load_user(id):
    return LoginUser.query.get(int(id))


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
    status = db.Column(db.String)
    time = db.Column(db.DateTime)
    psid = db.Column(db.String, db.ForeignKey('users.psid'))

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
    def find_by_user_id(cls, psid):
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


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User


class OrderSchema(ma.ModelSchema):
    class Meta:
        model = Order
    user = ma.Nested(UserSchema)


class LoginUserSchema(ma.ModelSchema):
    class Meta:
        model = LoginUser
