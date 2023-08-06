# coding=utf-8

from .. import celery
from mercury.services.notification import find_notifications_to_dispatch, update_notification

from datetime import datetime
from base64 import b64decode
from os import linesep

from flask_mail import Mail, Message

mail = Mail()


def init_app(app):
    """Initalizes the application with the extension.

    :param app: The Flask application object.
    """
    mail.init_app(app)


@celery.task()
def route_notifications():
    """Celery task routine to find and route notifications to dispatch to correct notification channel
    (executed by celery worker).

    :return: Operations logs.
    """
    notifications = find_notifications_to_dispatch()
    if notifications is None or notifications.count() < 1:
        return 'Nothing to dispatch.'
    result = ''
    for notification in notifications:
        result = f'{result}{linesep}{route_notification(notification)}'
    return result


def route_notification(notification):
    """Routes a notification to correct notification channel.

    :param notification: Notification to route to correct notification channel.
    :return: Operations logs.
    """
    return {
        'email': route_notification_mail(notification)
    }.get(notification['category'], 'email')


def route_notification_mail(notification):
    """Routes a notification to mail notification channel.

    :param notification: Notification to route to mail notification channel.
    :return: Operations logs.
    """
    recipients = notification['recipients']
    if isinstance(recipients, str):
        recipients = [recipients]
    msg = Message(recipients=recipients, subject=notification['subject'],
                  body=notification.get('body'), html=notification.get('html'),
                  cc=notification.get('cc'), bcc=notification.get('bcc'), reply_to=notification.get('reply_to'))
    try:
        attachments = notification.get('attachments')
        if attachments is not None:
            [msg.attach(filename=attachment.get('filename'), content_type=attachment.get('content_type'),
                        data=b64decode(attachment['data'])) for attachment in attachments]
    except Exception as ex:
        raise Exception(f'Mail attachments with _id {notification["_id"]} failed to load at '
                        f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}!{linesep}Detail: {str(ex)}')
    try:
        mail.send(msg)
    except Exception as ex:
        raise Exception(f'Dispatch mail with _id {notification["_id"]} failed at '
                        f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}!{linesep}Detail: {str(ex)}')
    success_msg = f'Successfully dispatched mail with _id {notification["_id"]} at ' \
                  f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.'
    try:
        notification['datetime_dispatch'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        result = update_notification(notification['_id'], notification)
        if result is None:
            raise Exception('Acknowledged: False.')
    except Exception as ex:
        raise Exception(f'Update mail datetime_dispatch with _id {notification["_id"]} failed at '
                        f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}!{linesep}Detail: {str(ex)}')
    return f'{success_msg}{linesep}Successfully updated mail datetime_dispatch with _id {notification["_id"]}.'
