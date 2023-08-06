# coding=utf-8

from mercury.services.database_nosql_mongo import db as mongo

from datetime import datetime
from bson import ObjectId

from flask_restful import fields, reqparse

"""Fields to marshal notification to JSON."""
notification_fields = {
    'category': fields.String,
    'datetime_schedule': fields.String,
    'datetime_dispatch': fields.String,
    'links': {
        # Replaces Notification ID with Notification Uri (HATEOAS) through endpoint 'notification'
        'self': fields.Url('notification')
    }
}


'''CRUD Functions'''


def get_request_parser(request_parser=None):
    """Get request parser for notification.

    :param request_parser: If exists, add request parser argument to request_parser param.
    :return: Notification request parser.
    """
    if request_parser is None:
        result = reqparse.RequestParser()
    else:
        result = request_parser
    result.add_argument('category', type=str, required=True, help='No notification category provided', location='json')
    result.add_argument('datetime_schedule', type=lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'), required=False,
                        help='No notification datetime_schedule provided', location='json')
    return result


def select_notification(id, user_id):
    """Get notification by id param and user_id.

    :param id: Notification's id to find.
    :param user_id: Notification's user_id to find.
    :return: Notification found or error 404.
    """
    return mongo.db.notification.find_one_or_404({'_id': ObjectId(id), 'user_id': user_id})


def select_notifications(user_id):
    """Get all notifications by user_id.

    :param user_id: Notification's user_id to find.
    :return: All notifications.
    """
    return mongo.db.notification.find({'user_id': user_id})


def insert_notification(notification, user_id):
    """Post new notification from notification param (MongoDB has limit of 16 megabytes per document) for user_id.

    :param notification: Notification to persist.
    :param user_id: Notification's user_id to persist.
    :return: Persisted notification's base informations or error.
    """
    notification['user_id'] = user_id
    notification['datetime_schedule'] = notification.get('datetime_schedule',
                                                         datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    notification.pop('_id', None)
    return {
        '_id': mongo.db.notification.insert_one(notification).inserted_id,
        'user_id': user_id,
        'category': notification['category'],
        'datetime_schedule': notification['datetime_schedule']
    }


def update_notification(id, notification, user_id=None):
    """Put the notification passed by notification param (MongoDB has limit of 16 megabytes per document) for user_id.

    :param id: Notification's id to find.
    :param user_id: Notification's user_id to find.
    :param notification: Notification to persist.
    :return: Persisted notification's base informations or error.
    """
    if user_id is None:
        user_id = notification['user_id']
    else:
        notification['user_id'] = user_id
    notification.pop('_id', None)
    notification_found = mongo.db.notification.find_one_or_404({'_id': ObjectId(id), 'user_id': user_id})
    if mongo.db.notification.update_one({'_id': notification_found['_id']}, {'$set': notification}).acknowledged:
        return {
            '_id': id,
            'user_id': user_id,
            'category': notification['category'],
            'datetime_schedule': notification.get('datetime_schedule', notification_found['datetime_schedule'])
        }
    else:
        return None


def delete_notification(id, user_id):
    """Delete the notification that have the passed notification id.

    :param id: Notification's id to find.
    :param user_id: Notification's user_id to find.
    :return: True if elimination was successful or False if elimination was not possible.
    """
    return mongo.db.notification.remove({'_id': ObjectId(id), 'user_id': user_id})['ok'] == 1.0


'''Other Functions'''


def find_notifications_to_dispatch():
    """Find all notifications that have datetime_schedule lower than now (local time) and that they haven't already been
     dispatched.

    :return: Cursor to manage notifications to dispatch.
    """
    return mongo.db.notification.find({
        'datetime_schedule': {'$lte': datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
        'datetime_dispatch': None
    })
