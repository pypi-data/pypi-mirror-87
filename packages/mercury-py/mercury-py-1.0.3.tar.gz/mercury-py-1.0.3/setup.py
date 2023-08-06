# coding=utf-8

from os import path
from setuptools import setup, find_packages

version = '1.0.3'

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='mercury-py',
    packages=find_packages(include=['mercury']),
    package_data={'mercury': ['static/favicon.ico']},
    include_package_data=True,
    zip_safe=False,
    version=version,
    description='mercury-py (Mercury for Python) is a Python based microservice that allow to manage scheduled '
                'notifications sending.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['notifications', 'authentication', 'email', 'sms', 'push notification', 'telegram'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Communications',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3'
    ],  # https://pypi.org/classifiers/
    author='Simone Perini',
    author_email='perinisimone98@gmail.com',
    license='BSD-3-Clause',
    url='https://github.com/CoffeePerry/mercury-py',
    download_url=f'https://github.com/CoffeePerry/mercury-py/archive/{version}.tar.gz',
    install_requires=[
        'Flask==1.1.2',
        'Flask-RESTful==0.3.8',
        'Flask-SQLAlchemy==2.4.4',
        'Flask-PyMongo==2.3.0',
        'Flask-JWT-Extended==3.25.0',
        'Flask-Mail==0.9.1',
        'celery==4.4.5'
    ]
)
