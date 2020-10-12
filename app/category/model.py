from uuid import uuid1
from sqlalchemy_json import NestedMutableJson
from app import db


class Category (db.Model):
    __tablename__ = 'categories'
    __table_args__ = (db.UniqueConstraint(
        'uuid', 'id', name='unique_category_items'),)
    id = db.Column(db.Integer, primary_key=True)
    created_time = db.Column(db.DateTime)
    catalog_uuid = db.Column(db.String, db.ForeignKey(
        'catalogs.uuid', ondelete='SET NULL', onupdate="CASCADE"), unique=True)
    uuid = db.Column(db.String, unique=True)
    title = db.Column(db.String)
    subtitle = db.Column(db.String)
    block = db.Column(NestedMutableJson)
    items = db.relationship(
        'Item', backref='category', lazy='select')

    def __init__(self, catalog_uuid, subtitle, title,  img):
        self.catalog_uuid = catalog_uuid,
        self.uuid = uuid1().hex
        self.title = title,
        self.subtitle = subtitle,
        self.img = img,
        self.block = self.make_category_block()

    # Class Methods

    def find_by_page_id(cls, page_id):
        return cls.query.filter_by(page_id=page_id).first()

    def find_by_uuid(cls, uuid):
        return cls.query.filter_by(uuid=uuid).first()

    def make_category_block(self):
        return {
            'payload': {
                'template_type': 'generic',
                'elements': []
            }

        }

    # Default Model Methods

    def update(self, changes):
        for key, val in changes.items():
            setattr(self, key, val)
        return self

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.remove(self)
        db.session.commit()
