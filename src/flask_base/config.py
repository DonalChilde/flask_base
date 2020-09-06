"""Default configuration
Use .secrets.cfg to override
"""


# {"name": "", "description": ""}
ROLES = [
    {"name": "admin", "description": "Admin users."},
    {"name": "user", "description": "Standard users"},
]


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
    SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/flask_base_db.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
