# coding=utf-8

from os import path

from flask_sqlalchemy import SQLAlchemy
from flask.cli import AppGroup

from os import makedirs

db = SQLAlchemy()
db_cli = AppGroup('database')


def init_app(app):
    """Initalizes the application database (SQL).

    :param app: The Flask application object.
    """
    db.init_app(app)
    app.cli.add_command(db_cli)

    try:
        # Ensure the database folder exists
        database_folder = path.join(app.instance_path, app.config['DATABASE_FOLDER'])
        if not path.isdir(database_folder):
            makedirs(database_folder)
            raise Exception(f'Directory not found, so just created: {database_folder}')
    except OSError as ex:
        app.logger.error(str(ex))
    except Exception as ex:
        app.logger.exception(str(ex))

    # Check if sql database exists
    if not path.isfile(app.config['DATABASE_FILENAME']):
        app.logger.warning(f'Database SQL not found! File: {app.config["DATABASE_FILENAME"]}')


@db_cli.command('create')
def create_database():
    """Create the database schema."""
    db.create_all()
    print('Database SQL created')


@db_cli.command('drop')
def drop_database():
    """Drop the database."""
    response = input('Are you really sure to delete the SQL database and all the data it contains? [Y/n]:')
    if response.lower() == 'y':
        db.drop_all()
        print('Database SQL dropped')
