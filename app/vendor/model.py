from sqlalchemy_json import NestedMutableJson
import datetime
from app import db


class Vendor(db.Model):
    __tablename__ = 'vendors'
    __table_args__ = (db.UniqueConstraint(
        'page_id', 'id', name='unique_vendor_customers'),)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)  # unique
    created_time = db.Column(db.DateTime)
    uid = db.Column(db.String, unique=True)  # unique
    comments = db.Column(NestedMutableJson)
    blocks = db.Column(NestedMutableJson)
    prices = db.Column(NestedMutableJson)
    arabic = db.Column(NestedMutableJson)
    page_access_token = db.Column(db.String)
    fcm_token = db.Column(db.String)
    is_setup = db.Column(db.Boolean)
    opening_hours = db.Column(db.Time)
    closing_hours = db.Column(db.Time)
    page_id = db.Column(db.String, unique=True)  # unique
    catalog = db.relationship('Catalog', backref='vendor', lazy='select')
    customers = db.relationship('Customer', backref='vendor', lazy='select')
    orders = db.relationship('Order', backref='vendor', lazy='select')

    def __init__(self, uid, page_id, name='', page_access_token='', fcm_token=''):
        self.name = name
        self.uid = uid
        self.comments = {}
        self.page_access_token = page_access_token
        self.fcm_token = fcm_token
        self.page_id = page_id
        self.created_time = datetime.datetime.utcnow()
        self.closing_hours = datetime.datetime.utcnow().time()
        self.opening_hours = datetime.datetime.utcnow().time()
        self.prices = {}
        self.arabic = {}
        self.is_setup = False

    def is_open(self):
        time = datetime.datetime.utcnow().time()
        print(self.closing_hours)
        print(self.opening_hours)
        print(time)
        if time > self.opening_hours:
            if self.closing_hours < self.opening_hours and time > self.closing_hours:
                return False
            elif self.closing_hours > self.opening_hours and time > self.closing_hours:
                return False
        elif time < self.opening_hours:
            if self.closing_hours < self.opening_hours and time > self.closing_hours:
                return False
        return True

    def set_working_hours(self, opening_hours, closing_hours):
        time_format = '%H:%M'
        self.closing_hours = datetime.datetime.strptime(
            closing_hours, time_format).time()
        self.opening_hours = datetime.datetime.strptime(
            opening_hours, time_format).time()

    @classmethod
    def find_by_page_id(cls, page_id):
        return cls.query.filter_by(page_id=page_id).first()

    @classmethod
    def find_by_uid(cls, uid):
        return cls.query.filter_by(uid=uid).first()

    def update(self, changes):
        for key, val in changes.items():
            setattr(self, key, val)
        return self

    def save(self):
        print('Vendor Saved')
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.remove(self)
        db.session.commit()
