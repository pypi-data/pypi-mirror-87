# coding=utf-8

from mercury.services import notification as services_notification
from mercury.services import user as services_user
from mercury.services.custom_exceptions import MethodVersionNotFound

from flask import abort, request
from flask_restful import Resource, marshal
from flask_jwt_extended import jwt_required, get_jwt_identity


class NotificationListAPI(Resource):
    decorators = [jwt_required]

    def __init__(self):
        """NotificationListAPI constructor."""
        self.reqparse = services_notification.get_request_parser()
        super(NotificationListAPI, self).__init__()

    def get(self, user_id):
        """GET

        :param user_id: User's id to find.
        :return: All notifications.
        """
        if request.headers.get('Accept-Version', '1.0') == '1.0':
            if get_jwt_identity() != user_id and (not services_user.check_if_user_is_admin(get_jwt_identity())):
                abort(401)
            return {'notifications': [marshal(notification, services_notification.notification_fields) for notification
                                      in services_notification.select_notifications(user_id)]}
        raise MethodVersionNotFound()

    def post(self, user_id):
        """POST

        :param user_id: User's id to find.
        :return: Persisted notification's base informations as JSON or error.
        """
        if request.headers.get('Accept-Version', '1.0') == '1.0':
            if get_jwt_identity() != user_id and (not services_user.check_if_user_is_admin(get_jwt_identity())):
                abort(401)
            if not request.json:
                abort(400)
            return {'notification': marshal(services_notification.insert_notification(request.json, user_id),
                                            services_notification.notification_fields)}, 201
        raise MethodVersionNotFound()


class NotificationAPI(Resource):
    decorators = [jwt_required]

    def __init__(self):
        """NotificationAPI constructor."""
        self.reqparse = services_notification.get_request_parser()
        super(NotificationAPI, self).__init__()

    def get(self, user_id, _id):
        """GET

        :param user_id: User's id to find.
        :param _id: Notification's id to find.
        :return: Notification found as JSON.
        """
        if request.headers.get('Accept-Version', '1.0') == '1.0':
            if get_jwt_identity() != user_id and (not services_user.check_if_user_is_admin(get_jwt_identity())):
                abort(401)
            return {'notification': marshal(services_notification.select_notification(_id, user_id),
                                            services_notification.notification_fields)}
        raise MethodVersionNotFound()

    def put(self, user_id, _id):
        """PUT

        :param user_id: User's id to find.
        :param _id: Notification's id to find.
        :return: Persisted notification's base informations as JSON or error.
        """
        if request.headers.get('Accept-Version', '1.0') == '1.0':
            if get_jwt_identity() != user_id and (not services_user.check_if_user_is_admin(get_jwt_identity())):
                abort(401)
            if not request.json:
                abort(400)
            result = services_notification.update_notification(_id, request.json, user_id)
            if result is None:
                return {'result': False}
            return {'notification': marshal(result, services_notification.notification_fields)}
        raise MethodVersionNotFound()

    def delete(self, user_id, _id):
        """DELETE

        :param user_id: User's id to find.
        :param _id: Notification's id to find.
        :return: True if elimination was successful or False if elimination was not possible.
        """
        if request.headers.get('Accept-Version', '1.0') == '1.0':
            if get_jwt_identity() != user_id and (not services_user.check_if_user_is_admin(get_jwt_identity())):
                abort(401)
            return {'result': services_notification.delete_notification(_id, user_id)}
        raise MethodVersionNotFound()
