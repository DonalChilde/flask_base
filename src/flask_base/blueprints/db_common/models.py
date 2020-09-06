import uuid
from datetime import datetime

import pytz
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import CHAR, TypeDecorator

from flask_base.extensions import db

# TODO make 'dev' only display of db tables and data.


def default_uuid():
    return str(uuid.uuid4())


class GUID(TypeDecorator):
    """Platform-independent GUID type.

    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.
    
    Source:
        https://gist.github.com/gmolveau/7caeeefe637679005a7bb9ae1b5e421e
    """

    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == "postgresql":
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value


# class Base(db.Model):

#     __abstract__ = True

#     id = db.Column(GUID(), primary_key=True, default=str(uuid.uuid4()))
#     created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
#     updated_at = db.Column(
#         db.DateTime,
#         default=db.func.current_timestamp(),
#         onupdate=db.func.current_timestamp(),
#     )


# class User(Base):

#     __tablename__ = "users"

#     username = db.Column(db.String, nullable=False, unique=True)
#     email = db.Column(db.String, nullable=False, unique=True)
#     encrypted_password = db.Column(db.String, nullable=False)

#     def set_password(self, password):
#         self.encrypted_password = bc.generate_password_hash(password)

#     def verify_password(self, password):
#         return bc.check_password_hash(self.encrypted_password, password)


class AwareDateTime(TypeDecorator):
    """
    A DateTime type which can only store tz-aware DateTimes.

    Source:
      https://gist.github.com/inklesspen/90b554c864b99340747e
    """

    impl = DateTime(timezone=True)

    def process_bind_param(self, value, dialect):
        if isinstance(value, datetime) and value.tzinfo is None:
            raise ValueError("{!r} must be TZ-aware".format(value))
        return value

    def __repr__(self):
        return "AwareDateTime()"


def tzware_datetime():
    """
    Return a timezone aware datetime.now

    :return: Datetime
    """
    return datetime.now(pytz.utc)


class ResourceMixin(object):
    # Keep track when records are created and updated.
    created_on = db.Column(AwareDateTime(), default=tzware_datetime)
    updated_on = db.Column(
        AwareDateTime(), default=tzware_datetime, onupdate=tzware_datetime
    )

    def save(self):
        """
        Save a model instance.

        :return: Model instance
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        Delete a model instance.

        :return: db.session.commit()'s result
        """
        db.session.delete(self)
        return db.session.commit()

    def __str__(self):
        """
        Create a human readable version of a class instance.

        :return: self
        """
        obj_id = hex(id(self))
        columns = self.__table__.c.keys()

        values = ", ".join("%s=%r" % (n, getattr(self, n)) for n in columns)
        return "<%s %s(%s)>" % (obj_id, self.__class__.__name__, values)
