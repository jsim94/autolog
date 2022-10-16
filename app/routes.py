# app > routes.py

from functools import wraps

from sqlalchemy.exc import IntegrityError
from flask import current_app as app, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required, login_user, logout_user

from app.forms import SignupForm, LoginForm
from app.models.users import User

from app.bcolors import bcolors


@app.before_request
def mark_console():
    '''debug purposes only'''
    if app.debug:
        print()
        if request.method == 'GET':
            print(f'####################### GET #########################')
        if request.method == 'POST':
            print(
                f'{bcolors.OKGREEN}####################### POST #########################{bcolors.ENDC}')
        if request.method == 'DELETE':
            print(
                f'{bcolors.FAIL}####################### DELETE #########################{bcolors.ENDC}')
        print()


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
    form = SignupForm()

    if form.validate_on_submit():
        try:
            user = User.signup(username=form.username.data,
                               email=form.email.data, password=form.password.data)
        except IntegrityError:
            flash("Username or email already taken", 'danger')
            return redirect(url_for('signup'))

        login_user(user, remember='remember')
        return redirect(url_for('profile.show', username=user.username))

    return render_template('home_form.html', form=form, signup=True)


@app.route('/login', methods=('GET', 'POST'))
@user_redirect
def login():
    '''GET returns login form, POST submits login parameters and redirects user to their profile page'''
    form = LoginForm()

    if form.validate_on_submit():
        user = User.validate(username=form.username.data,
                             password=form.password.data)
        if user:
            login_user(user, remember='remember')
            return redirect(url_for('profile.show', username=user.username))
        flash("Invalid username or password", 'danger')
        return redirect(url_for('login'))

    return render_template('home_form.html', form=form, signup=False)


@app.route('/logout')
@login_required
def logout():
    '''Log out user'''
    logout_user()
    flash('Successfully logged out')
    return redirect(url_for('homepage'))
