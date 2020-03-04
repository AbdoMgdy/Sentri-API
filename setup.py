from flask import Flask, request, render_template, url_for, redirect, current_app
from flask_sqlalchemy import SQLAlchemy
# from flask_restx import Api
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO, emit, join_room, leave_room, send
from flask_marshmallow import Marshmallow
import eventlet
db = SQLAlchemy()
ma = Marshmallow()
# eventlet.monkey_patch()  # to enable message queue for Flask-SocketIO


def create_app(env=None):
    from config import config_by_name
    from webhook import routes as webhook_routes
    from vendor import routes as vendor_routes
    from customer import routes as customer_routes
    from order import routes as order_routes
    from db import db
    app = Flask(__name__, static_folder='static',
                static_url_path='', template_folder='templates')
    # message_queue=os.environ.get('REDIS_URL', None)
    app.config.from_object(config_by_name[env or "test"])
    socketio = SocketIO(app, cors_allowed_origins="*")
    migrate = Migrate(app, db, compare_type=True)
    jwt = JWTManager(app)
    CORS(app)
    app.register_blueprint(vendor_routes.vendor_bp)
    app.register_blueprint(webhook_routes.webhook_bp)
    app.register_blueprint(order_routes.order_bp)
    app.register_blueprint(customer_routes.customer_bp)
    return app
