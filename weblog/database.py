#coding=utf8

from sqlalchemy.pool import NullPool
from flask.ext.sqlalchemy import SQLAlchemy
from . import app


"""
class NullPoolSQLAlchemy(SQLAlchemy):
    def apply_driver_hacks(self, app, info, options):
        super(NullPoolSQLAlchemy, self).apply_driver_hacks(app, info, options)
        options['poolclass'] = NullPool
        del options['pool_size']

db = NullPoolSQLAlchemy(app)
"""

db = SQLAlchemy(app)
