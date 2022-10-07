# app > models > mixins.py

import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from app import db


def generate_uuid_hex():
    return uuid.uuid4().hex


class timestamps(object):
    '''Mixin for creation date column'''
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow())
    last_edit = db.Column(db.DateTime, nullable=False,
                          default=datetime.utcnow(), onupdate=datetime.utcnow())


class uuid_pk(object):
    '''Mixin for an auto increment int primary key and a unique UUID'''
    pk = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(32), unique=True,
                   nullable=False, default=generate_uuid_hex)
