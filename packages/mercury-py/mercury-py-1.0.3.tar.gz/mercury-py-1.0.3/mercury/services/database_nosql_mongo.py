# coding=utf-8

from flask_pymongo import PyMongo

db = PyMongo()


def init_app(app):
    """Initalizes the application database MongoDB (NoSQL).

    :param app: The Flask application object.
    """
    db.init_app(app)
