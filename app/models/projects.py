# app > models > projects.py

from sqlalchemy.dialects.postgresql import ARRAY, ENUM
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.exc import NoResultFound

from app import db
from .mixins import base, timestamps
from .enums import PrivacyStatus, Drivetrain
from .users import User
from app.bcolors import bcolors


class Project(base, timestamps, db.Model):
    '''Project car class. Each project car has one owner'''
    __tablename__ = 'projects'

    user_pk = db.Column(db.Integer, db.ForeignKey(
        'users.pk', ondelete="cascade"), nullable=False)
    private = db.Column(ENUM(PrivacyStatus), nullable=False,
                        server_default="PUBLIC")
    model_id = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(30))
    description = db.Column(db.String(500))
    mods = db.Column(MutableList.as_mutable(ARRAY(db.String(50))), default=[])

    year = db.Column(db.Text, nullable=True)
    make = db.Column(db.Text, nullable=True)
    model = db.Column(db.Text, nullable=True)

    horsepower = db.Column(db.Integer)
    torque = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    drivetrain = db.Column(ENUM(Drivetrain))
    engine_size = db.Column(db.Float)

    pictures = db.relationship(
        'ProjectPicture', cascade="all,delete-orphan", backref='project')
    updates = db.relationship(
        'Update', cascade="all,delete-orphan", backref='project')
    comments = db.relationship(
        'Comment', cascade="all,delete-orphan", backref='project')

    @property
    def w2p(self):
        '''Return weight to power ratio rounded to two digits'''
        try:
            return round((self.weight / self.horsepower), 2)
        except ZeroDivisionError:
            return 0

    def __repr__(self):
        return '<Project %r>' % self.name

    @classmethod
    def get_by_name(cls, name):
        '''Get user object by username search or return none.'''
        project = cls.query.filter_by(name=name).first()
        if project:
            return project
        raise NoResultFound()

    @classmethod
    def create(cls, user_pk, name, description, model_id, private, year, make, model, horsepower, torque, weight, drivetrain, engine_size):
        '''Create new project '''

        project = Project(
            user_pk=user_pk,
            name=name,
            description=description,
            model_id=model_id if model_id else -1,
            private=private,
            year=year,
            make=make,
            model=model,
            horsepower=horsepower,
            torque=torque,
            weight=weight,
            drivetrain=drivetrain,
            engine_size=engine_size
        )

        db.session.add(project)
        cls._commit()
        return project

    def add_follow(self, user):
        '''Add a user to a projects followers list

        :param project: project instance
        :param id: id of project instance
        '''
        self.followers.append(user)
        self._commit()

    def remove_follow(self, user):
        '''Remove a user to a projects followers list

        :param project: project instance
        :param id: id of project instance
        '''
        self.followers.remove(user)
        self._commit()

    def add_mod(self, mod):
        '''Add mod to projects mod list'''
        self.mods.append(mod)
        self._commit()

    def delete_mod(self, index):
        '''Takes index of mod to delete and deletes it from project.mods'''
        self.mods.pop(index)
        self._commit()


class Update(base, timestamps, db.Model):
    '''Table that holds update posts to a project'''
    __tablename__ = 'updates'

    project_pk = db.Column(db.Integer, db.ForeignKey(
        'projects.pk', ondelete="cascade"))
    title = db.Column(db.String(60))
    content = db.Column(db.String(1000), nullable=False)

    @classmethod
    def create(cls, project_id, title, content):
        '''Creates a new row in updates table and appends it to a project'''
        project = Project.get_by_id(project_id)
        update = Update(project_pk=project.pk, title=title.rstrip(),
                        content=content.rstrip())
        db.session.add(update)
        cls._commit()


class Comment(base, timestamps, db.Model):
    '''Table that holds comments other users can make for a project '''
    __tablename__ = 'comments'

    user_pk = db.Column(db.Integer, db.ForeignKey(
        'users.pk', ondelete="cascade"), nullable=False)
    project_pk = db.Column(db.Integer, db.ForeignKey(
        'projects.pk', ondelete="cascade"), nullable=False)
    content = db.Column(db.String(300), nullable=False)

    @classmethod
    def create(cls, user_id, project_id, content):
        '''Creates a new comment and attaches a user and project to it'''
        user = User.get_by_id(user_id)
        project = Project.get_by_id(project_id)

        comment = Comment(
            user_pk=user.pk, project_pk=project.pk, content=content)
        db.session.add(comment)
        cls._commit()
        return comment
