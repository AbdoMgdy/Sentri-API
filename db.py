import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.dialects.postgresql import JSONB

db = SQLAlchemy()
ma = Marshmallow()
