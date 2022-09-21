# app > models > projects.py

from sqlalchemy.dialects.postgresql import ARRAY, ENUM
from sqlalchemy.exc import IntegrityError

from app import db
from .mixins import uuid_pk, timestamps
from .enums import PrivacyStatus, Drivetrain


class Project(uuid_pk, timestamps, db.Model):
    '''Project car class. Each project car has one owner'''
    __tablename__ = 'projects'

    user_pk = db.Column(db.Integer, db.ForeignKey(
        'users.pk', ondelete="cascade"), nullable=False)
    private = db.Column(ENUM(PrivacyStatus), nullable=False,
                        server_default="PUBLIC")

    model_id = db.Column(db.Integer)
    name = db.Column(db.String(30))
    description = db.Column(db.String(500))
    mods = db.Column(ARRAY(db.String(50)))

    year = db.Column(db.Integer)
    make = db.Column(db.Text)
    model = db.Column(db.Text)

    horsepower = db.Column(db.Integer)
    torque = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    drivetrain = db.Column(ENUM(Drivetrain))
    w2p = db.Column(db.Float)
    engine_size = db.Column(db.Integer)

    pictures = db.relationship('ProjectPicture', backref='project')
    followers = db.relationship(
        'User', secondary='followers', backref='following')
    updates = db.relationship('Update', backref='project')
    comments = db.relationship('Comment', backref='project')

    def calc_weight_to_power(self):
        '''Return weight to power ratio rounded to two digits'''
        return round((self.weight / self.horsepower), 2)

    w2p = property(calc_weight_to_power)

    @classmethod
    def create(cls, user_pk, name, description, model_id, private, year, make, model, horsepower, torque, weight, drivetrain, engine_size):
        '''Create new project '''

        project = Project(
            user_pk=user_pk,
            name=name,
            description=description,
            model_id=model_id,
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

    def __repr__(self):
        return '<Project %r>' % self.name


class Follower(db.Model):
    '''Table that connects a user other than the owner to a project for the sake of following the project'''
    __tablename__ = 'followers'

    user_pk = db.Column(db.Integer, db.ForeignKey(
        'users.pk', ondelete="cascade"), primary_key=True)
    project_pk = db.Column(db.Integer, db.ForeignKey(
        'projects.pk', ondelete="cascade"), primary_key=True)


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
