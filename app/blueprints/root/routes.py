# app > routes.py
from functools import wraps

from sqlalchemy.exc import IntegrityError, NoResultFound
from flask import current_app as app, render_template, redirect, url_for, flash, request, g
from flask_login import current_user, login_required, login_user, logout_user

from . import bp
from app import lm
from app.forms import SignupForm, LoginForm
from app.models.users import User

from app.bcolors import bcolors


@lm.user_loader
def load_user(user_id):
    '''Get logged in user before request. Also adds user to flask global and updates last login time for user'''
    try:
        user = User.get_by_id(user_id)
        user.update_login_time()
        g.current_user = user
    except NoResultFound:
        g.current_user = None
        return
    return user


@bp.before_request
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


@bp.route('/')
@user_redirect
def homepage():
    '''Displays homepage'''
    return render_template('home.html')


@bp.route('/signup', methods=('GET', 'POST'))
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
            return redirect(url_for('root.signup'))

        login_user(user, remember='remember')
        return redirect(url_for('profile.show', username=user.username))

    return render_template('home_form.html', form=form, signup=True)


@bp.route('/login', methods=('GET', 'POST'))
@user_redirect
def login():
    '''GET returns login form, POST submits login parameters and redirects user to their profile page'''
    form = LoginForm()

    if form.validate_on_submit():
        try:
            user = User.authenticate(username=form.username.data,
                                     password=form.password.data)
        except NoResultFound:
            user = None

        if user:
            login_user(user, remember='remember')
            return redirect(url_for('profile.show', username=user.username))
        flash("Invalid username or password", 'danger')
        return redirect(url_for('root.login'))

    return render_template('home_form.html', form=form, signup=False)


@bp.route('/logout')
@login_required
def logout():
    '''Log out user'''
    logout_user()
    setattr(g, 'current_user', None)
    flash('Successfully logged out')
    return redirect(url_for('root.homepage'))
