''' Blueprint for project routes '''
# app > project > __init__.py

from flask import Blueprint

bp = Blueprint('project', __name__, template_folder='templates',
               static_folder='static')

from . import routes
