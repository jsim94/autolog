''' Blueprint for profile routes '''
# app > profile > __init__.py

from flask import Blueprint

bp = Blueprint('profile', __name__, template_folder='templates',
               static_folder='static')

from . import routes
