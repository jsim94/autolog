# app > models > projects.py

from sqlalchemy.dialects.postgresql import ARRAY, ENUM
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.exc import IntegrityError
from flask_login import current_user

from app import db
from .mixins import uuid_pk, timestamps
from .enums import PrivacyStatus, Drivetrain

from app.bcolors import bcolors


class Project(uuid_pk, timestamps, db.Model):
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
    w2p = db.Column(db.Float)
    engine_size = db.Column(db.Float)

    pictures = db.relationship('ProjectPicture', backref='project')
    updates = db.relationship('Update', backref='project')
    comments = db.relationship('Comment', backref='project')

    def calc_weight_to_power(self):
        '''Return weight to power ratio rounded to two digits'''
        try:
            return round((self.weight / self.horsepower), 2)
        except ZeroDivisionError:
            return 0

    w2p = property(calc_weight_to_power)

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

        try:
            db.session.add(project)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return
        return project

    @classmethod
    def get_by_name(cls, name):
        '''Get user object by username search or return none.'''
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_by_uuid(cls, uuid):
        '''Get user object by uuid search or return none.'''
        return cls.query.filter_by(id=uuid).first()

    def owner_required(func):
        '''Decorator that checks if flask_login.current_user is the user of the project'''

        def inner(self, *args, **kwargs):
            return func(self, *args, **kwargs) if self.user == current_user else 403
        return inner

    @owner_required
    def update(self, owner):
        '''Method to take in updates to a project and commit them to the database. 
        --
        At this time all this does is commit the update to the database. The actual update is handled in project/routes.py with 'form.populate_obj()' --
        '''
        db.session.commit()
        return 200

    @owner_required
    def add_mod(self, mod):
        '''Add mod to projects mod list'''
        try:
            self.mods.append(mod)
            db.session.commit()
        except:
            return 500

        return 200

    @owner_required
    def delete_mod(self, index):
        '''Takes index of mod to delete and deletes it from project.mods'''
        try:
            self.mods.pop(index)
            db.session.commit()
        except IndexError:
            return 404
        except:
            return 500
        return 200

    @owner_required
    def delete(self):
        '''Check auth of user and either return 403 or 200'''
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            return 500
        return 200

    def __repr__(self):
        return '<Project %r>' % self.name


class Update(uuid_pk, timestamps, db.Model):
    '''Table that holds update posts to a project'''
    __tablename__ = 'updates'

    project_pk = db.Column(db.Integer, db.ForeignKey(
        'projects.pk', ondelete="cascade"))
    content = db.Column(db.Text, nullable=False)


class Comment(uuid_pk, timestamps, db.Model):
    '''Table that holds comments other users can make for a project '''
    __tablename__ = 'comments'

    user_pk = db.Column(db.Integer, db.ForeignKey(
        'users.pk', ondelete="cascade"), nullable=False)
    project_pk = db.Column(db.Integer, db.ForeignKey(
        'projects.pk', ondelete="cascade"), nullable=False)
    content = db.Column(db.Text, nullable=False)
