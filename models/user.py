from db import db
from sqlalchemy.dialects.postgresql import
import requests
from models.bot import Bot


class User(Bot, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    psid = db.Column(db.Integer)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    phone_number = db.Column(db.Integer)
    address = db.Column(db.String)
    orders = db.relationship('Order', lazy='select')

    def __init__(self, psid):
        super().__init__()
        self.psid = psid
        self.first_name = ''
        self.last_name = ''
        self.phone_number = ''
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
        self.first_name = result['first_name']
        self.last_name = result['last_name']

    def add(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.remove(self)
        db.session.commit()
