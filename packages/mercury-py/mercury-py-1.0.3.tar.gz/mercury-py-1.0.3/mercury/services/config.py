# coding=utf-8

from os import path


class Config(object):
    def __init__(self, app=None):
        """Config constructor.

        :param app: Application in which to inject the development settings.
        """
        self.app = app

        self.DEBUG = False

        # Flask
        self.SECRET_KEY = None

        # Flask-JWT-Extended
        self.JWT_SECRET_KEY = self.SECRET_KEY

        # DBs
        self.DATABASE_FOLDER = 'sqldb'
        self.DATABASE_FILENAME = path.join(self.app.instance_path, self.DATABASE_FOLDER, 'mercury.sqlite3')
        self.SQLALCHEMY_DATABASE_URI = f'sqlite:///{self.DATABASE_FILENAME}'
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
        self.MONGO_URI = None

        # Celery - for Tasks
        self.BROKER_URL = None
        self.CELERY_RESULT_BACKEND = self.MONGO_URI
        self.CELERY_LOGS_FOLDER = 'logs'
        self.CELERY_BEAT_FOLDER = 'celerybeat'

        # Email
        self.MAIL_SERVER = None
        self.MAIL_PORT = None
        self.MAIL_USE_TLS = True
        self.MAIL_USERNAME = None
        self.MAIL_PASSWORD = None
        self.MAIL_DEFAULT_SENDER = (None, None)
