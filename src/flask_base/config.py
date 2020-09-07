"""Default configuration
Use .secrets.cfg to override

Sources:
    https://medium.com/@aswens0276/using-pytest-to-setup-dynamic-testing-for-your-flask-apps-postgres-database-locally-and-with-39a14c3dc421
    https://xvrdm.github.io/2017/07/03/testing-flask-sqlalchemy-database-with-pytest/
"""
import os

# {"name": "", "description": ""}
ROLES = [
    {"name": "admin", "description": "Admin users."},
    {"name": "user", "description": "Standard users"},
]


def get_env_variable(name):
    try:
        return os.environ.get(name)
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)


def create_postgresql_db_url(user, pw, url, db):
    return f"postgresql://{user}:{pw}@{url}/{db}"


class Config(object):
    # Flask Settings
    DEBUG = False
    TESTING = False
    SECRET_KEY = "change_me"

    # SqlAlchemy Settings
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    """

    """

    # Flask Settings
    DEBUG = False
    TESTING = False

    # DATABASE_URI = "mysql://user@localhost/foo"


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/flask_base_db.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Test data usually in secrets.cfg
    # An initial admin user.
    SEED_ADMIN_USERNAME = "test_i_am_groot"
    SEED_ADMIN_EMAIL = "test_i_am_groot@example.com"
    SEED_ADMIN_PASSWORD = "test_password1234"
