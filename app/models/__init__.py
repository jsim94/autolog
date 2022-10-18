'''Initializes SQLalchemy models from each module'''
# app > models > __init__.py

from flask_sqlalchemy import models_committed

from .users import *
from .projects import *
from .images import *


@models_committed.connect
def committed(sender, changes):
    '''Calls the __commit_<change>__ method on a model when a certain commit happens'''
    for obj, change in changes:
        if change == 'insert' and hasattr(obj, '__commit_insert__'):
            obj.__commit_insert__()
        if change == 'udpate' and hasattr(obj, '__commit_update__'):
            obj.__commit_update__()
        if change == 'delete' and hasattr(obj, '__commit_delete__'):
            obj.__commit_delete__()
