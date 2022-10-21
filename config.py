"""Flask configuration variables."""
from os import environ


class Config:
    """Set Flask configuration from .env file."""

    # General Config
    SECRET_KEY = environ.get(
        'SECRET_KEY', "72b13325f1a7c86d105120dcb57bd97e36a86157a4abb8e3fe66eaa0395097ab")
    FLASK_APP = environ.get('FLASK_APP')
    TESTING = bool(environ.get('TESTING', 'False'))
    UPLOAD_FOLDER = environ.get('UPLOAD_FOLDER', 'app/static/uploads')

    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # Database
    SQLALCHEMY_DATABASE_URI = (
        environ.get('DATABASE_URL', 'postgresql:///modlog'))
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Dropzone
    DROPZONE_ALLOWED_FILE_TYPE = 'image'
    DROPZONE_MAX_FILES = 20
    DROPZONE_ENABLE_CSRF = True
    DROPZONE_MAX_FILE_SIZE = 10
