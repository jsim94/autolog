"""Flask configuration variables."""
from os import environ


class Config:
    """Set Flask configuration from .env file."""

    # General Config
    SECRET_KEY = environ.get(
        'SECRET_KEY', "01ce6ef7-db1a-4bb9-ba8c-83cb64b7f0c3")
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV', 'DEVELOPMENT')
    UPLOAD_FOLDER = 'app/static/assets'

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
