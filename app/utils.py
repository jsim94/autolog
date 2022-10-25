import os
import uuid
from functools import wraps
from PIL import Image

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


def generate_uuid_hex():
    return uuid.uuid4().hex


def save_image_file(file, fn, path, tb_size):
    file.seek(0)
    img = Image.open(file.stream)
    try:
        img.save(os.path.join(path, fn),
                 optimize=True, quality=75)
    except FileNotFoundError:
        if os.path.exists(path):
            raise
        os.makedirs(path)
        img.save(os.path.join(path, fn),
                 optimize=True, quality=75)
    if tb_size:
        img.thumbnail(tb_size)
        tb_path = os.path.join(path, 'thumbnails')
        try:
            img.save(os.path.join(tb_path, fn))
        except FileNotFoundError:
            if os.path.exists(tb_path):
                raise
            os.makedirs(tb_path)
            img.save(os.path.join(tb_path, fn))


def delete_image_file(path, fn):

    file = os.path.join(path, fn)
    file_tb = os.path.join(path, 'thumbnails', fn)

    if os.path.isfile(file):
        os.remove(file)
    if os.path.isfile(file_tb):
        os.remove(file_tb)
