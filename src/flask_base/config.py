"""Default configuration
Use env var to override
"""
import os

# ENV = os.getenv("FLASK_ENV")
# DEBUG = ENV == "development"


class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = "sqlite:///:memory:"
    SECRET_KEY = "change_me"


class ProductionConfig(Config):
    DATABASE_URI = "mysql://user@localhost/foo"


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
