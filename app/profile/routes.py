# app > profile > routes.py

from base64 import urlsafe_b64decode
from flask import render_template, redirect, g, url_for, abort
from flask_login import login_required, current_user

from app.models.users import User

from . import bp


@bp.url_value_preprocessor
def get_profile_owner(endpoint, values):
    g.user = User.get_by_username(username=values.get(
        'username', current_user.username if hasattr('current_user', 'username') else None))
    if not g.user:
        abort(404)


@bp.route('/<username>')
def show(username):
    '''Retrieves the profile page for the user by username if the requesting client has access to the page, otherwise returns 403.'''

    owner = False
    if g.user == current_user:
        owner = True

    if g.user.private is 'PRIVATE' and owner is False:
        abort(403)

    return render_template('profile.html', owner=owner)


@bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    '''GET returns a profile edit page and POST will update profile'''
    return f'Not yet implemented - User: {g.user}'
