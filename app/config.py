
import os
from typing import List, Type

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    CONFIG_NAME = "base"
    SECRET_KEY = os.urandom(32)
    USE_MOCK_EQUIVALENCY = False
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 'sqlite:///data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False


class DevelopmentConfig(BaseConfig):
    CONFIG_NAME = "dev"
    DEBUG = True


class TestingConfig(BaseConfig):
    CONFIG_NAME = "test"
    DEBUG = True
    TESTING = True


class ProductionConfig(BaseConfig):
    CONFIG_NAME = "prod"
    JWT_ACCESS_TOKEN_EXPIRES = False
    JWT_SECRET_KEY = os.urandom(32)
    CORS_HEADERS = 'Content-Type'


EXPORT_CONFIGS: List[Type[BaseConfig]] = [
    DevelopmentConfig,
    TestingConfig,
    ProductionConfig,
]
config_by_name = {cfg.CONFIG_NAME: cfg for cfg in EXPORT_CONFIGS}
