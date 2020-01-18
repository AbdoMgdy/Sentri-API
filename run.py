from app import app
from db import db, ma


db.init_app(app)
ma.init_app(app)


@app.before_first_request
def create_table():
    db.create_all()
