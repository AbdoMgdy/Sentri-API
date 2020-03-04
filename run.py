from setup import create_app
from db import db, ma

app = create_app(env='prod')

db.init_app(app)
ma.init_app(app)


@app.before_first_request
def create_table():
    db.create_all()
