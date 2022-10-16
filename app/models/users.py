# app > models > users.py

from datetime import datetime

from flask import g
from sqlalchemy.exc import NoResultFound
from sqlalchemy.dialects.postgresql import ENUM
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

from app import db, lm
from .mixins import base
from .enums import PrivacyStatus


from app.bcolors import bcolors


bcrypt = Bcrypt()


@lm.user_loader
def load_user(user_id):
    '''Get logged in user before request. Also adds user to flask global and updates last login time for user'''
    try:
        user = User.get_by_id(user_id)
        g.current_user = user
    except NoResultFound:
        g.current_user = None
        return
    try:
        user.update_login_time()
        db.session.commit()
    except:
        db.session.rollback()
        raise
    return user


class User(UserMixin, base, db.Model):
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
    def validate(cls, password, user=None, username=None, id=None):
        '''Check if password hash matches and returns the user or None

        :param user: Passed user object to validate password for
        :param id: Id of user to validate password for
        :param username: str:username of user to validate password for
        '''
        if not user:
            if username:
                user = cls.get_by_username(username)
            if id:
                user = cls.get_by_id(id)

        if user:
            return user if bcrypt.check_password_hash(user.password, password) else None
        return None

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
        db.session.add(user)
        cls._commit()
        return user

    def edit(self, username, new_password, email):
        '''Edits user object. Returns user'''
        password = bcrypt.generate_password_hash(
            new_password).decode('UTF-8')
        return super().edit(obj=self, username=username, password=password, email=email)


class Follow(db.Model):
    '''Table that connects a user to a project for the sake of following the project'''
    __tablename__ = 'followers'

    user_pk = db.Column(db.Integer, db.ForeignKey(
        'users.pk', ondelete="cascade"), primary_key=True)
    project_pk = db.Column(db.Integer, db.ForeignKey(
        'projects.pk', ondelete="cascade"), primary_key=True)
