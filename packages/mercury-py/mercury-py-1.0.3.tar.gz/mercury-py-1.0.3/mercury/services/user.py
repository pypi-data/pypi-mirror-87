# coding=utf-8

from mercury.models.user import User
from mercury.services.database_sql import db, db_cli

from datetime import timedelta

from werkzeug.exceptions import BadRequest, Unauthorized, Forbidden
from flask_restful import fields, reqparse, inputs
from flask_jwt_extended import create_access_token
from click import argument

"""Fields to marshal user to JSON."""
user_fields = {
    'username': fields.String,
    'creation_datetime': fields.String,
    'active': fields.Boolean,
    'links': {
        'self': fields.Url('user')  # Replaces User ID with User Uri (HATEOAS) through endpoint 'user'
    }
}

"""Fields to marshal user login info to JSON."""
user_login_fields = dict(user_fields)
user_login_fields['access_token'] = fields.String


def get_request_parser(request_parser=None, is_login_request=False):
    """Get request parser for user.

    :param request_parser: If exists, add request parser argument to request_parser param.
    :param is_login_request: If True, add request parser argument password to request_parser param.
    :return: User request parser.
    """
    if request_parser is None:
        result = reqparse.RequestParser()
    else:
        result = request_parser
    result.add_argument('username', type=str, required=True, help='No user username provided', location='json')
    if is_login_request:
        result.add_argument('password', type=str, required=True, help='No user password provided', location='json')
    result.add_argument('active', type=inputs.boolean, required=False, help='No user active provided', location='json')
    return result


'''CRUD Functions'''


def select_user(id):
    """Get user by id param.

    :param id: User's id to find.
    :return: User found.
    """
    return User.query.get_or_404(id)


def select_users():
    """Get all users.

    :return: All users.
    """
    return User.query.all()


def insert_user(username):
    """Post new user from username param.

    :param username: User's username to persist.
    :return: Persisted user or error.
    """
    user = User()
    user.username = username
    user.generate_password()
    db.session.add(user)
    db.session.commit()
    return user


def update_user(user):
    """Put the user passed by user param.

    :param user: User to persist.
    :return: Persisted user or error.
    """
    if user is None:
        return None
    db.session.commit()
    return user


def delete_user(id):
    """Delete the user that have the passed user id.

    :param id: User's id to find.
    :return: True if elimination was successful or False if elimination was not possible.
    """
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return True


'''Other Functions'''


def login_user(user):
    """Login user from user param.

    :param user: User to login.
    :return: User's access_token or error.
    """
    username = user.get('username')
    if username is None:
        raise BadRequest('Missing username parameter')
    password = user.get('password')
    if password is None:
        raise BadRequest('Missing password parameter')
    db_user = User.query.filter(User.username == username).scalar()
    if db_user and db_user.verify_password(password):
        if not db_user.active:
            raise Forbidden('User inactive')
        db_user.access_token = create_access_token(identity=db_user.id, expires_delta=timedelta(days=1))
        return db_user
    else:
        raise Unauthorized('Bad username or password')


def check_if_user_is_admin(id):
    """Check if user by id param is admin.

    :param id: User's id to find.
    :return: Outcome of the comparison, True if user is admin, otherwise False.
    """
    user = User.query.get(id)
    if user is None:
        return False
    return user.admin


@db_cli.command('register')
@argument('username')
def register_user(username):
    """Register new user.

    :param username: New user's username.
    """
    if not username:
        print('Please, enter an unique Username.')
    else:
        response = input(f'Are you really sure to register new user {username}? [Y/n]:')
        if response.lower() == 'y':
            print('Creation in progress...')
            user = insert_user(username)
            print(f'{user} successfully created')
        else:
            print('Aborted.')
