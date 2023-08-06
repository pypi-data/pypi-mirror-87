# coding=utf-8

from celery import Celery
from celery.schedules import crontab

from os import path, makedirs

celery = Celery(__name__)


def init_app(app):
    """Initalizes the application with the extension.

    :param app: The Flask application object.
    """
    celery.conf.broker_url = app.config['BROKER_URL']
    celery.conf.update(app.config)
    celery.config_from_object(CeleryBeatConfig())  # Load Celery Beat instance config

    try:
        # Ensure the celery beat folder exists
        celery_beat_folder = path.join(app.instance_path, app.config['CELERY_BEAT_FOLDER'])
        if not path.isdir(celery_beat_folder):
            makedirs(celery_beat_folder)
            raise Exception(f'Directory not found, so just created: {celery_beat_folder}')
    except OSError as ex:
        app.logger.error(str(ex))
    except Exception as ex:
        app.logger.exception(str(ex))

    try:
        # Ensure the celery logs folder exists
        celery_logs_folder = path.join(app.instance_path, app.config['CELERY_LOGS_FOLDER'])
        if not path.isdir(celery_logs_folder):
            makedirs(celery_logs_folder)
            raise Exception(f'Directory not found, so just created: {celery_logs_folder}')
    except OSError as ex:
        app.logger.error(str(ex))
    except Exception as ex:
        app.logger.exception(str(ex))

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask


class CeleryBeatConfig(object):
    def __init__(self):
        """CeleryBeatConfig constructor"""
        self.CELERY_TASK_SERIALIZER = 'json'
        self.CELERY_RESULT_SERIALIZER = 'json'
        self.CELERY_ACCEPT_CONTENT = ['json']
        self.CELERY_IMPORTS = ('mercury.services.tasks.notification', )
        self.CELERY_TIMEZONE = 'UTC'
        self.CELERY_TASK_RESULT_EXPIRES = 30

        self.CELERYBEAT_SCHEDULE = {
            'route_notifications': {
                'task': 'mercury.services.tasks.notification.route_notifications',
                'schedule': crontab(minute='*'),  # Every minute
            }
        }
