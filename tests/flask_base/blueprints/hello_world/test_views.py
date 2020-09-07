import pytest
from flask_base.config import TestingConfig


def test_example(app):

    print("config\n", *[f"{k}: {v}\n" for k, v in app.config.items()])
    assert app.config["ENV"] == "development"


def test_true(app):

    assert True


def test_hello_world(client):

    response = client.get("/hello_world/")
    print(response.data)
    assert response.status_code == 200
    assert b"Hello, World! --Bob" in response.data
