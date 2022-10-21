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


def assert_in_range(value, min, max):
    '''Returns True if value is within min and max range'''
    if value < min:
        raise AssertionError(
            f'Value {value} too low. Must be between {min} and {max}')
    if value > max:
        raise AssertionError(
            f'Value {value} too high. Must be between {min} and {max}')
    return True
