# coding=utf-8

from mercury.services import user as services_user
from mercury.services.custom_exceptions import MethodVersionNotFound

from flask import abort, request
from flask_restful import Resource, marshal
from flask_jwt_extended import jwt_required, get_jwt_identity


class UserListAPI(Resource):
    decorators = [jwt_required]

    def __init__(self):
        """UserListAPI constructor."""
        self.reqparse = services_user.get_request_parser()
        super(UserListAPI, self).__init__()

    def get(self):
        """GET

        :return: All users.
        """
        if request.headers.get('Accept-Version', '1.0') == '1.0':
            if not services_user.check_if_user_is_admin(get_jwt_identity()):
                abort(401)
            return {'users': [marshal(user, services_user.user_fields) for user in services_user.select_users()]}
        raise MethodVersionNotFound()

    def post(self):
        """POST

        :return: Persisted user's JSON or error.
        """
        if request.headers.get('Accept-Version', '1.0') == '1.0':
            if not services_user.check_if_user_is_admin(get_jwt_identity()):
                abort(401)
            if not request.json:
                abort(400)
            user = {key: value for key, value in self.reqparse.parse_args().items() if value is not None}
            return {'user': marshal(services_user.insert_user(user['username']), services_user.user_fields)}, 201
        raise MethodVersionNotFound()


class UserAPI(Resource):
    decorators = [jwt_required]

    def __init__(self):
        """UserAPI constructor."""
        self.reqparse = services_user.get_request_parser()
        super(UserAPI, self).__init__()

    def get(self, id):
        """GET

        :param id: User's id to find.
        :return: User found as JSON.
        """
        if request.headers.get('Accept-Version', '1.0') == '1.0':
            if get_jwt_identity() != id and (not services_user.check_if_user_is_admin(get_jwt_identity())):
                abort(401)
            return {'user': marshal(services_user.select_user(id), services_user.user_fields)}
        raise MethodVersionNotFound()

    def put(self, id):
        """PUT

        :param id: User's id to find.
        :return: Persisted user's base informations as JSON or error.
        """
        if request.headers.get('Accept-Version', '1.0') == '1.0':
            if get_jwt_identity() != id and (not services_user.check_if_user_is_admin(get_jwt_identity())):
                abort(401)
            if not request.json:
                abort(400)
            user = services_user.select_user(id)
            [user.__setattr__(key, value) for key, value in self.reqparse.parse_args().items() if value is not None]
            return {'user': marshal(services_user.update_user(user), services_user.user_fields)}
        raise MethodVersionNotFound()

    def delete(self, id):
        """DELETE

        :param id: User's id to find.
        :return: True if elimination was successful or False if elimination was not possible.
        """
        if request.headers.get('Accept-Version', '1.0') == '1.0':
            if get_jwt_identity() != id and (not services_user.check_if_user_is_admin(get_jwt_identity())):
                abort(401)
            return {'result': services_user.delete_user(id)}
        raise MethodVersionNotFound()


class UserLoginAPI(Resource):
    def __init__(self):
        """UserLoginAPI constructor."""
        self.reqparse = services_user.get_request_parser(is_login_request=True)
        super(UserLoginAPI, self).__init__()

    def post(self):
        """Post

        :return: User's access_token as JSON or error.
        """
        if request.headers.get('Accept-Version', '1.0') == '1.0':
            if not request.json:
                abort(400)
            user = {key: value for key, value in self.reqparse.parse_args().items() if value is not None}
            return {'user': marshal(services_user.login_user(user), services_user.user_login_fields)}
        raise MethodVersionNotFound()
