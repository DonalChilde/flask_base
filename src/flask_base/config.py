"""Default configuration
Use env var to override
"""
import os

# ENV = os.getenv("FLASK_ENV")
# DEBUG = ENV == "development"


class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # DATABASE_URI = "sqlite:///:memory:"
    SECRET_KEY = "change_me"


class ProductionConfig(Config):
    pass
    # DATABASE_URI = "mysql://user@localhost/foo"


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
