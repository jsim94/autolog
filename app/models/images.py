# app > models > images.py
from werkzeug.utils import secure_filename

from . import db
from .mixins import base, timestamps


class ImageBase(base, timestamps, object):
    '''Base picture class'''
    upload_ip = db.Column(db.Text, nullable=False)
    extension = db.Column(db.Text, nullable=False)

    @property
    def filename(self):
        return f'{self.id}.{self.extension}'

    @classmethod
    def create(cls, filename, project, ip):
        '''USE THIS to add any image to the database'''
        ext = secure_filename(filename).split('.')[-1]
        if ext not in ['png', 'jpg', 'jpeg', 'gif']:
            raise ValueError('Incorrect Filetype')

        picture = cls(upload_ip=ip, project_pk=project.pk, extension=ext)
        db.session.add(picture)
        cls._commit()

        return picture


class ProfilePicture(ImageBase, db.Model):
    '''Model for users' profile pictures'''
    __tablename__ = 'profile_pictures'

    user_pk = db.Column(db.Integer, db.ForeignKey(
        'users.pk', ondelete="cascade"))


class ProjectPicture(ImageBase, db.Model):
    '''Model for pictures that are attached to projects'''
    __tablename__ = 'project_pictures'

    project_pk = db.Column(db.Integer, db.ForeignKey(
        'projects.pk', ondelete="cascade"), nullable=False)
    description = db.Column(db.String(120))
