import pytest

from flask_base.app import create_app
from flask_base.extensions import db as flask_db

# from dotenv import load_dotenv


@pytest.fixture(scope="session")
def app():
    # load_dotenv(".testenv")
    test_app = create_app(testing=True)
    return test_app


@pytest.fixture
def client(app):
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture
def db(app):
    with app.app_context():
        yield flask_db
        # db.create_all()
        # yield db
        # db.drop_all()
        # db.session.commit()
