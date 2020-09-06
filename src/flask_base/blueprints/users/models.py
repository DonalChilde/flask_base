import uuid
from datetime import datetime
from typing import Optional

import pytz

from flask_base.extensions import db
from flask_base.blueprints.db_common.models import (
    GUID,
    AwareDateTime,
    ResourceMixin,
    default_uuid,
)

# TODO password hash

user_role_table = db.Table(
    "user_role",
    db.Model.metadata,
    db.Column("user_id", GUID(), db.ForeignKey("user.id"), primary_key=True),
    db.Column("role_id", GUID(), db.ForeignKey("role.id"), primary_key=True),
)


class User(ResourceMixin, db.Model):
    id = db.Column(GUID(), primary_key=True, default=default_uuid)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True)
    # Activity tracking.
    sign_in_count = db.Column(db.Integer, nullable=False, default=0)
    current_sign_in_on = db.Column(AwareDateTime())
    current_sign_in_ip = db.Column(db.String(45))
    last_sign_in_on = db.Column(AwareDateTime())
    last_sign_in_ip = db.Column(db.String(45))
    roles = db.relationship("Role", secondary=user_role_table, backref="users")

    def update_activity_tracking(self, ip_address):
        """
        Update various fields on the user that's related to meta data on their
        account, such as the sign in count and ip address, etc..

        :param ip_address: IP address
        :type ip_address: str
        :return: SQLAlchemy commit results
        """
        self.sign_in_count += 1

        self.last_sign_in_on = self.current_sign_in_on
        self.last_sign_in_ip = self.current_sign_in_ip

        self.current_sign_in_on = datetime.datetime.now(pytz.utc)
        self.current_sign_in_ip = ip_address

        return self.save()

    @classmethod
    def make_user(cls, username, email, password, active=True):
        # TODO do checks to make sure username and email are unique.
        # or maybe just username. share emails?
        user = cls(username=username, email=email, password=password, active=active)
        user.save()
        return user

    @classmethod
    def make_admin_user(cls, username, email, password, active=True):
        admin = cls.make_user(username, email, password, active)
        admin_role = Role.query.filter_by(name="admin").one_or_none()
        if admin_role is None:
            # TODO change to proper exception
            raise Exception("Admin role not found. Did you init the roles?")
        admin.roles.append(admin_role)
        admin.save()
        return admin

    def __repr__(self):
        return f"<User {self.username}"


class Role(ResourceMixin, db.Model):
    id = db.Column(GUID(), primary_key=True, default=default_uuid)
    name = db.Column(db.String(), nullable=False, unique=True)
    description = db.Column(db.String())


# class UserRole(ResourceMixin, db.Model):
#     user_id = db.Column(GUID(), db.ForeignKey("user.id"), primary_key=True)
#     role_id = db.Column(GUID(), db.ForeignKey("role.id"), primary_key=True)

