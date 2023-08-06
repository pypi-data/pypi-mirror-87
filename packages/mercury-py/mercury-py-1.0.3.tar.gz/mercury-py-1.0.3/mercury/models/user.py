# coding=utf-8

from mercury.services.database_sql import db

from typing import Final
from datetime import datetime
from secrets import token_hex, compare_digest


class User(db.Model):
    _PASSWORD_STORED_MAX_LENGTH: Final = 128  # Password max bytes length: 64 bytes (512 bit) * 2 = 128 bytes (because hex stored)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(254), index=True, unique=True, nullable=False)
    password = db.Column(db.String(_PASSWORD_STORED_MAX_LENGTH), nullable=False)
    creation_datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    active = db.Column(db.Boolean, nullable=False, default=True)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    access_token = None

    def __repr__(self):
        """Returns user representation.

        :return: Username that represent user.
        """
        return '<User %r>' % self.username

    def generate_password(self):
        """Generate a password and save it to user."""
        self.password = token_hex(int(self._PASSWORD_STORED_MAX_LENGTH / 2))

    def verify_password(self, password):
        """Verify the passed password against user's password.

        :param password: Password to compare.
        :return: Outcome of the comparison, True if password is correct, otherwise False.
        """
        return compare_digest(self.password, password)
