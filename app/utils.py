from functools import wraps
from flask import abort, g


def owner_required(func):
    '''Decorator to return a 403 error if the current user is not authorized to access endpoint'''
    @wraps(func)
    def inner(*args, **kwargs):
        if not g.get('owner'):
            abort(403)
        return func(*args, **kwargs)
    return inner
