# app > profile > routes.py

from sqlalchemy.exc import NoResultFound, IntegrityError
from flask import render_template, redirect, g, url_for, abort, flash
from flask_login import login_required, current_user

from app.models.users import User
from app.forms import UserEdit

from . import bp


@bp.url_value_preprocessor
def get_profile_owner(endpoint, values):
    try:
        g.user = User.get_by_username(username=values['username'])
        g.owner = True if g.user == current_user else False
    except NoResultFound:
        abort(404)
    except KeyError:
        return


@bp.route('/<username>')
def show(username):
    '''Retrieves the profile page for the user by username if the requesting client has access to the page, otherwise returns 403.'''
    # if user not found return 404
    if not g.user:
        abort(404)
    # return 403 is profile is private and the current_user is not the owner
    if g.user.private == 'PRIVATE' and g.owner is False:
        abort(403)
    return render_template('profile.html')


@bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    '''GET returns a profile edit page and POST will edit profile'''
    form = UserEdit(obj=current_user)

    if form.validate_on_submit():
        username = form.username.data
        old_password = form.old_password.data
        new_password = form.password.data
        email = form.email.data

        if User.authenticate(user=current_user, password=old_password):
            try:
                user = User.edit(
                    obj=current_user,
                    username=username,
                    new_password=new_password,
                    email=email
                )
                if user:
                    flash('Profile successfully updated', 'info')
                    return redirect(url_for('profile.show', username=user.username))
                flash('Error occured', 'error')
            except IntegrityError:
                flash('Username or email already taken', 'danger')
        else:
            flash('Wrong password', 'warning')
    return render_template('profile_edit.html', form=form, user=current_user)


@bp.route('/<username>/following')
def show_following(username):
    return render_template('profile_following.html')
