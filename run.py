from app import app, socketio
from db import db, ma, login


db.init_app(app)
ma.init_app(app)
login.init_app(app)
login.login_view = 'login'


@app.before_first_request
def create_table():
    db.create_all()
