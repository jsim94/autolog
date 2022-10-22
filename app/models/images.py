# app > models > images.py
import os
from PIL import Image

from flask import current_app
from werkzeug.utils import secure_filename
from app import db
from .mixins import base, timestamps


if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
    os.mkdir(current_app.config['UPLOAD_FOLDER'])
    print('Created user upload directory:',
          current_app.config['UPLOAD_FOLDER'])


class ImageBase(base, timestamps, object):
    '''Base picture class'''
    upload_ip = db.Column(db.Text, nullable=False)
    extension = db.Column(db.Text, nullable=False)

    @property
    def filename(self):
        return f'{self.id}.{self.extension}'

    @classmethod
    def create(cls, file, project, ip):
        '''USE THIS to add any image to the database'''
        ext = secure_filename(file.filename).split('.')[-1]
        if ext not in ['png', 'jpg', 'jpeg', 'gif']:
            raise ValueError('Incorrect Filetype')

        picture = cls(upload_ip=ip, project_pk=project.pk, extension=ext)
        db.session.add(picture)
        cls._commit()
        try:
            file.seek(0)
            img = Image.open(file.stream)
            try:
                img.save(os.path.join(cls.PATH, picture.filename),
                         optimize=True, quality=75)
            except FileNotFoundError:
                if os.path.exists(cls.PATH):
                    raise
                os.makedirs(cls.PATH)
                img.save(os.path.join(cls.PATH, picture.filename),
                         optimize=True, quality=75)

            if cls.TB_SIZE:
                img.thumbnail(cls.TB_SIZE)
                tb_path = os.path.join(cls.PATH, 'thumbnails')
                try:
                    img.save(os.path.join(tb_path, picture.filename))
                except FileNotFoundError:
                    if os.path.exists(tb_path):
                        raise
                    os.makedirs(tb_path)
                    img.save(os.path.join(tb_path, picture.filename))

        except:
            db.session.delete(picture)
            db.session.commit()
            raise
        return picture

    def __commit_delete__(self):
        '''Delete the associated files on session commit'''

        file = f'{self.PATH}{self.filename}'
        file_tb = f'{self.PATH}thumbnails/{self.filename}'

        if os.path.isfile(file):
            os.remove(file)
        if os.path.isfile(file_tb):
            os.remove(file_tb)


class ProfilePicture(ImageBase, db.Model):
    '''Model for users' profile pictures'''
    PATH = os.path.join(
        current_app.config['UPLOAD_FOLDER'], 'profile_pictures/')

    __tablename__ = 'profile_pictures'

    user_pk = db.Column(db.Integer, db.ForeignKey(
        'users.pk', ondelete="cascade"))
    upload_ip = db.Column(db.Text, nullable=False)


class ProjectPicture(ImageBase, db.Model):
    '''Model for pictures that are attached to projects'''
    PATH = os.path.join(
        current_app.config['UPLOAD_FOLDER'], 'project_pictures/')
    TB_SIZE = 350, 350

    __tablename__ = 'project_pictures'

    project_pk = db.Column(db.Integer, db.ForeignKey(
        'projects.pk', ondelete="cascade"), nullable=False)
    description = db.Column(db.String(120))
