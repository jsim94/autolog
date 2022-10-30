"""Flask configuration variables."""
from os import environ
from enum import Enum


class DefaultConfig(object):
    # General Config
    SECRET_KEY = environ.get(
        'SECRET_KEY', "SET A CUSTOM KEY IN ENV!!")
    FLASK_APP = environ.get('FLASK_APP')
    UPLOAD_FOLDER = 'app/static/assets/uploads'
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # Database
    SQLALCHEMY_DATABASE_URI = ('postgresql://')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Dropzone
    DROPZONE_ALLOWED_FILE_TYPE = 'image'
    DROPZONE_MAX_FILES = 15
    DROPZONE_ENABLE_CSRF = True
    DROPZONE_MAX_FILE_SIZE = 10


class ProdConfig(DefaultConfig):
    DEBUG = False

    SECRET_KEY = environ.get(
        'SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = (
        environ.get('DATABASE_URL'))


class DevConfig(DefaultConfig):
    DEBUG = True

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = (
        environ.get('DATABASE_URL', 'postgresql:///modlog'))


class TestConfig(DefaultConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'postgresql:///modlog_test'
    UPLOAD_FOLDER = 'tests/uploads'
