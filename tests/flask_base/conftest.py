import pytest

from flask_base.app import create_app

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
