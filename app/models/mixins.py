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

    @classmethod
    def edit(cls, obj=None, id=None, keys=None, **kwargs):
        '''Edits an exising row in a table with passed args. Returns the edited object

        :param obj: 
            Accepts an object to be modified. Can be called from an instance method override or classmethod
        :param id: 
            The id of the object to be modified. Must be called as a class method
        :param keys: 
            A dict of key values to update the object with with.
        :param **kwargs:
            passed attributes to update on the object.        
        '''
        if not obj:
            obj = cls.get_by_id(id)

        for key, value in keys.items() if keys else kwargs.items():
            if key in cls.__table__.columns:
                if value is not None:
                    setattr(obj, key, value)
            else:
                msg = 'No attr \'' + key + '\' found in table columns'
                raise AttributeError(msg)
        if 'is_edited' in cls.__table__.columns:
            obj.is_edited = True
        cls._commit()
        return obj

    @classmethod
    def delete(cls, obj=None, id=None):
        '''Deletes a row from table

        :param obj: 
            Accepts an object to be deleted. Can be called from an instance method override
        :param id: 
            The id of the object to be deleted. Must be called as a class method
        '''
        if not obj:
            obj = cls.get_by_id(id)

        db.session.delete(obj)
        cls._commit()


class timestamps(object):
    '''Mixin for creation date and auto last_edit date columns'''
    created_at = db.Column(db.DateTime, nullable=False,
                           default=func.current_timestamp())
    last_edit = db.Column(db.DateTime, nullable=False,
                          default=func.now(), onupdate=func.current_timestamp())
    is_edited = db.Column(db.Boolean, default=False)
