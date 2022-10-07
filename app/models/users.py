# app > models > users.py

from datetime import datetime

from flask import g
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql import ENUM
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, login_user, logout_user

from app import db, lm
from .mixins import uuid_pk
from .enums import PrivacyStatus

from app.bcolors import bcolors


bcrypt = Bcrypt()


@lm.user_loader
def load_user(user_id):
    '''Get logged in user before request. Also adds user to flask global and updates last login time for user'''
    user = User.get_by_id(user_id)
    if user:
        g.current_user = user
        user.update_login_time()
        try:
            db.session.commit()
        except Exception as e:
            print('ERROR WHEN UPDATING USER LOGIN', str(e))
            db.session.rollback()
    else:
        g.current_user = None
    return user


class User(UserMixin, uuid_pk, db.Model):
    '''User model'''
    __tablename__ = 'users'

    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow())
    last_login = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow())
    private = db.Column(ENUM(PrivacyStatus),
                        nullable=False, default="PUBLIC")
    profile_picture = db.Column(
        db.Text, default="../default.png")

    projects = db.relationship('Project', cascade="all,delete", backref='user')
    following = db.relationship(
        'Project', secondary='followers', cascade="all,delete", backref='followers')
    comments = db.relationship('Comment', cascade="all,delete", backref='user')

    def __repr__(self):
        return '<User %r>' % self.username

    @classmethod
    def get_by_username(cls, username):
        '''Get user object by username search or return none.'''
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_by_id(cls, id):
        '''Get user object by uuid search or return none.'''
        return cls.query.filter_by(id=id).first()

    def validate_password(self, password):
        '''Check if password hash matches and returns True or False'''
        return bcrypt.check_password_hash(self.password, password)

    def update_login_time(self):
        '''Update last login time'''
        self.last_login = datetime.utcnow()

    @classmethod
    def signup(cls, username, email, password):
        '''Create new user:
            Hash password and add the new user to session. Returns None if duplicate email or username is found'''
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        user = User(
            username=username,
            email=email,
            password=hashed_pwd
        )

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return

        login_user(user, remember='remember')
        return user

    @classmethod
    def login(cls, username=None, password=None, user=None):
        ''' Logs a user in and returns the user if username and password match or if the user object is passed in.'''
        if user:
            login_user(user, remember='remember')
            return user

        if username and password:
            user = cls.get_by_username(username)
            if user and user.validate_password(password):
                login_user(user, remember='remember')
                return user
        return

    def update(self, username, old_password, new_password, email):
        ''' Validates password and updates user profile. Returns user if update is successful'''
        if not self.validate_password(old_password):
            return

        self.username = username
        self.password = bcrypt.generate_password_hash(
            new_password).decode('UTF-8')
        self.email = email

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return
        return self

    def logout(self):
        '''Logsout current_user'''
        logout_user()

    def add_follow(self, project):
        '''Add a project to a users following list'''
        try:
            self.following.append(project)
            db.session.commit()
            return 200
        except:
            db.session.rollback()
            return 500

    def remove_follow(self, project):
        '''Remove a project to a users following list'''
        try:
            self.following.remove(project)
            db.session.commit()
            return 200
        except:
            db.session.rollback()
            return 500


class Follow(db.Model):
    '''Table that connects a user to a project for the sake of following the project'''
    __tablename__ = 'followers'

    user_pk = db.Column(db.Integer, db.ForeignKey(
        'users.pk', ondelete="cascade"), primary_key=True)
    project_pk = db.Column(db.Integer, db.ForeignKey(
        'projects.pk', ondelete="cascade"), primary_key=True)
