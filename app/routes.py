# app > routes.py

import os
from functools import wraps
from flask import current_app as app, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from app.forms import UserForm, LoginForm
from app.models.users import User

from app.bcolors import bcolors


@app.before_request
def clear_console():
    '''debug purposes only'''
    print(
        f'{bcolors.OKBLUE}#####################################################################{bcolors.ENDC}')


def user_redirect(f):
    """Redirect user to their profile when accessing home routes while logged in"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if hasattr(current_user, 'username'):
            return redirect(url_for('profile.show', username=current_user.username))
        return f(*args, **kwargs)
    return wrapper


@app.route('/')
@user_redirect
def homepage():
    '''Displays homepage'''
    return render_template('home.html')


@app.route('/signup', methods=('GET', 'POST'))
@user_redirect
def signup():
    '''GET returns signup form, POST submits new user into database and redirects user to profile page'''
    form = UserForm()

    if form.validate_on_submit():
        user = User.signup(username=form.username.data,
                           email=form.email.data, password=form.password.data)
        if not user:
            flash("Username or email already taken", 'danger')
            return redirect(url_for('signup'))

        User.login(user=user)
        return redirect(url_for('profile.show', username=user.username))

    return render_template('home_form.html', form=form, signup=True)


@app.route('/login', methods=('GET', 'POST'))
@user_redirect
def login():
    '''GET returns login form, POST submits login parameters and redirects user to their profile page'''
    form = LoginForm()

    if form.validate_on_submit():
        user = User.login(username=form.username.data,
                          password=form.password.data)
        if not user:
            flash("Invalid username or password", 'danger')
            return redirect(url_for('login'))
        return redirect(url_for(
            'profile.show',
            username=user.username))

    return render_template('home_form.html', form=form, signup=False)


@app.route('/logout')
@login_required
def logout():
    '''Log out user'''
    current_user.logout()
    flash('Successfully logged out')
    return redirect(url_for('homepage'))
