''' Blueprint for home routes '''
# app > home > __init__.py

from flask import Blueprint

bp = Blueprint('root', __name__, template_folder='templates',
               static_folder='static')

from . import routes
