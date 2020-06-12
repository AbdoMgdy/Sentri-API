from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager

from flask_marshmallow import Marshmallow
import eventlet

db = SQLAlchemy()
ma = Marshmallow()


def create_app(env=None):
    from .config import config_by_name
    from .routes import register_routes
    app = Flask(__name__, static_folder='static',
                static_url_path='', template_folder='templates')
    api = Api(app)
    app.config.from_object(config_by_name[env or "test"])
    migrate = Migrate(app, db, compare_type=True)
    jwt = JWTManager(app)
    CORS(app)
    register_routes(app, api)
    db.init_app(app)
    ma.init_app(app)
    db.create_all()
    @app.route("/health")
    def health():
        return jsonify("healthy")
    return app
