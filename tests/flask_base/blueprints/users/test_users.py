import pytest

from flask_base.blueprints.users.models import Role, User
from flask_base.config import TestingConfig


def test_admin_role(db):
    result = Role.query.filter_by(name="admin").one_or_none()
    assert result is not None


def test_user_role(db):
    result = Role.query.filter_by(name="user").one_or_none()
    assert result is not None


def test_admin_seed(db):
    admin = User.query.filter_by(
        username=TestingConfig.SEED_ADMIN_USERNAME
    ).one_or_none()
    assert admin is not None
    admin_role = Role.query.filter_by(name="admin").one_or_none()
    assert admin_role is not None
    assert admin_role in admin.roles

