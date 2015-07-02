#!/usr/bin/env python

from weblog.database import db

if __name__ == '__main__':
    db.create_all()
