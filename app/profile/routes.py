# app > profile > routes.py

from flask import render_template, redirect, g, url_for, abort, flash
from flask_login import login_required, current_user

from app.models.users import User
from app.forms import UserUpdate

from . import bp


@bp.url_value_preprocessor
def get_profile_owner(endpoint, values):
    g.user = User.get_by_username(username=values.get(
        'username', current_user.username if hasattr('current_user', 'username') else None))


@bp.route('/<username>')
def show(username):
    '''Retrieves the profile page for the user by username if the requesting client has access to the page, otherwise returns 403.'''

    # if user not found return 404
    if not g.user:
        abort(404)

    # determine if current_user is the owner of g.user and return 403 if current_user doesn't have access
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
    form = UserUpdate(obj=current_user)

    if form.validate_on_submit():
        username = form.username.data
        old_password = form.old_password.data
        new_password = form.password.data
        email = form.email.data

        user = current_user.update(
            username=username,
            old_password=old_password,
            new_password=new_password,
            email=email
        )

        if user:
            flash('Profile successfully updated')
            return redirect(url_for('profile.show', username=user.username))
        flash('Error occurred')

    return render_template('edit.html', form=form, user=current_user)
