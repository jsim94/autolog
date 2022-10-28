# app > models > mixins.py
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.exc import NoResultFound

from . import db
from app.utils import generate_uuid_hex


class base(object):
    '''Mixin for an auto increment int primary key and a unique hex UUID'''
    pk = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(32), unique=True,
                   nullable=False, default=generate_uuid_hex)

    @staticmethod
    def _commit():
        '''Tries to commit session to db and rollsback session on exception'''
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise

    @classmethod
    def get_by_id(cls, id):
        '''Get row by id'''
        result = cls.query.filter_by(id=id).first()
        if result:
            return result
        raise NoResultFound()

    def edit(self, keys=None, **kwargs):
        '''Edits an exising row in a table with passed args and commits. Returns the edited object

        :param keys: 
            A dict of key values to update the object with with.
        :param **kwargs:
            passed attributes to update on the object.        
        '''
        def set_attrs(values):
            for key, value in values.items():
                if key in self.__table__.columns:
                    if bool(value):
                        setattr(self, key, value)
                else:
                    msg = 'No attr \'' + key + '\' found in table columns'
                    raise AttributeError(msg)
        if keys:
            set_attrs(keys)
        if kwargs:
            set_attrs(kwargs)

        if 'is_edited' in self.__table__.columns:
            self.is_edited = True
        self._commit()
        return self

    def delete(self):
        '''Deletes a row from table and commits'''
        db.session.delete(self)
        self._commit()


class timestamps(object):
    '''Mixin for creation date and auto last_edit date columns'''
    created_at = db.Column(db.DateTime, nullable=False,
                           default=func.current_timestamp())
    last_edit = db.Column(db.DateTime, nullable=False,
                          default=func.now(), onupdate=func.current_timestamp())
    is_edited = db.Column(db.Boolean, default=False)
