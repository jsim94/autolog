# app > models > images.py
from PIL import Image

from app import db
from .mixins import uuid_pk, timestamps


class ProfilePicture(uuid_pk, timestamps, db.Model):
    '''Model for users' profile pictures'''
    __tablename__ = 'profile_pictures'

    user_pk = db.Column(db.Integer, db.ForeignKey(
        'users.pk', ondelete="cascade"))
    uploaded_at = db.Column(db.Text, nullable=False)
    image_name = db.Column(db.Text, nullable=False)


class ProjectPicture(uuid_pk, timestamps, db.Model):
    '''Model for pictures that are attached to projects'''
    __tablename__ = 'project_pictures'

    image_name = db.Column(db.Text, nullable=False)
    uploaded_at = db.Column(db.Text, nullable=False)
    project_pk = db.Column(db.Integer, db.ForeignKey(
        'projects.pk', ondelete="cascade"), nullable=False)
    description = db.Column(db.String(120))
