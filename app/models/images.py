# app > models > images.py
import os
import warnings
from PIL import Image

from flask import current_app
from werkzeug.utils import secure_filename
from sqlalchemy.orm.exc import NoResultFound

from app import db
from .mixins import uuid_pk, timestamps


class ProfilePicture(uuid_pk, timestamps, db.Model):
    '''Model for users' profile pictures'''
    __tablename__ = 'profile_pictures'

    user_pk = db.Column(db.Integer, db.ForeignKey(
        'users.pk', ondelete="cascade"))
    upload_ip = db.Column(db.Text, nullable=False)


class ProjectPicture(uuid_pk, timestamps, db.Model):
    '''Model for pictures that are attached to projects

    !!Always create a new picture through the 'add' method to ensure a filename is generated properly!!
    '''
    __tablename__ = 'project_pictures'

    project_pk = db.Column(db.Integer, db.ForeignKey(
        'projects.pk', ondelete="cascade"), nullable=False)
    upload_ip = db.Column(db.Text, nullable=False)
    extension = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(120))

    def make_filename(self):
        return f'{self.id}.{self.extension}'

    filename = property(make_filename)

    @classmethod
    def get_by_id(cls, id):
        '''Get user object by uuid search or return none.'''
        return cls.query.filter_by(id=id).first()

    @classmethod
    def add(cls, file, project, ip):
        '''Method to add a user uploaded image to their project. Also handles adding the picture and its thumbnail to storage'''
        PATH = os.path.join(
            current_app.config['UPLOAD_FOLDER'], 'project_pictures/')
        SIZE = 350, 350

        ext = secure_filename(file.filename).split('.')[-1]
        if ext not in ['png', 'jpg', 'jpeg', 'gif']:
            raise ValueError('Incorrect Filetype')

        try:
            picture = cls(upload_ip=ip, project_pk=project.pk, extension=ext)
            db.session.add(picture)
            db.session.commit()
        except:
            db.session.rollback()
            raise

        try:
            file.seek(0)
            img = Image.open(file.stream)
            img.save(os.path.join(PATH, picture.filename),
                     optimize=True, quality=75)
            img.thumbnail(SIZE)
            img.save(os.path.join(PATH, 'thumbnails/', picture.filename))
        except:
            db.session.delete(picture)
            db.session.commit()
            raise

        return picture

    def delete(self):
        '''Method to delete a picture from database and remove it from storage'''
        PATH = os.path.join(
            current_app.config['UPLOAD_FOLDER'], 'project_pictures/')

        file = f'{PATH}{self.filename}'
        file_tb = f'{PATH}/thumbnails/{self.filename}'

        if os.path.isfile(file) and os.path.isfile(file_tb):
            os.remove(file)
            os.remove(file_tb)
        else:
            raise FileNotFoundError

        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
            raise
