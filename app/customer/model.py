import datetime
from app import db


class Customer(db.Model):
    __tablename__ = 'customers'
    __table_args__ = (db.UniqueConstraint(
        'psid', 'id', name='unique_customer_orders'),)
    id = db.Column(db.Integer, primary_key=True)
    psid = db.Column(db.String, unique=True)
    name = db.Column(db.String(80))
    phone_number = db.Column(db.String)
    address = db.Column(db.String)
    created_time = db.Column(db.DateTime)
    orders = db.relationship('Order', backref='customer', lazy='select')
    page_id = db.Column(db.String, db.ForeignKey('vendors.page_id'))

    def __init__(self, psid, page_id):
        self.psid = psid
        self.page_id = page_id
        self.created_time = datetime.datetime.utcnow()
        self.name = ''
        self.phone_number = 0
        self.address = ''

    @classmethod
    def find_by_psid(cls, psid):
        return cls.query.filter_by(psid=psid).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.remove(self)
        db.session.commit()
