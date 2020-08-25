import pytest


def test_example(app):
    print("config", *[f"{k}: {v}" for k, v in app.config.items()])
    assert False


def test_true(app):
    assert True
