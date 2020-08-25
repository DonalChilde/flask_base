import pytest

# from dotenv import load_dotenv

from flask_base.app import create_app


@pytest.fixture(scope="session")
def app():
    # load_dotenv(".testenv")
    app = create_app(testing=True)
    return app
