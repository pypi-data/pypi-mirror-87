# coding=utf-8

from mercury import create_app
from mercury.services.tasks import celery  # Necessary for app.celery invocation (worker & beat)

app = create_app()
