"""Flask configuration variables."""
from os import environ


class Config:
    """Set Flask configuration from .env file."""

    # General Config
    SECRET_KEY = environ.get(
        'SECRET_KEY', "01ce6ef7-db1a-4bb9-ba8c-83cb64b7f0c3")
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV', 'DEVELOPMENT')

    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # Database
    SQLALCHEMY_DATABASE_URI = (
        environ.get('DATABASE_URL', 'postgresql:///modlog'))
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
