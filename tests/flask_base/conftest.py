import pytest
from dotenv import load_dotenv

from flask_base.app import create_app
from flask_base.config import TestingConfig
from flask_base.extensions import db as flask_db
from flask_base.blueprints.db_common.cli_cmd import seed_admin, seed_roles

# Flask does not load .flaskenv unless using the Flask command.
# So load it manually during pytest.
load_dotenv(".flaskenv")

# from dotenv import load_dotenv


@pytest.fixture(scope="session")
def app():
    # load_dotenv(".testenv")
    test_app = create_app(config_class=TestingConfig())
    return test_app


@pytest.fixture
def client(app):
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture
def db(app):
    assert "TestingConfig" in app.config["CONFIG_OBJECT"]
    with app.app_context():
        flask_db.drop_all(app=app)
        flask_db.create_all(app=app)
        seed_roles()
        seed_admin(app)
        yield flask_db
        flask_db.drop_all()
    # db.create_all()
    # yield db
    # db.drop_all()
    # db.session.commit()


@pytest.yield_fixture
def app_builder():
    """
    # Note: not in use
    Source:
        https://medium.com/@aswens0276/using-pytest-to-setup-dynamic-testing-for-your-flask-apps-postgres-database-locally-and-with-39a14c3dc421
    """

    def _app(config_class):
        app = create_app(config_class=config_class)
        # app.test_request_context().push()

        if config_class is TestingConfig:

            # always starting with an empty DB
            flask_db.drop_all()
            flask_db.create_all()

        return app

    yield _app
    flask_db.session.remove()
    if str(flask_db.engine.url) == TestingConfig.SQLALCHEMY_DATABASE_URI:
        flask_db.drop_all()
