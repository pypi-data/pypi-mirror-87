# coding=utf-8

from flask_jwt_extended import JWTManager

jwt = JWTManager()


def init_app(app):
    """Initalizes the application auth.

    :param app: The Flask application object.
    """
    jwt.init_app(app)
