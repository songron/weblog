#coding=utf8

from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqlamodel import ModelView
from myapp import app
from data import (db, Category, Tag, Article, Comment, User,\
                    Link, BlackList, Subscriber)


class MyModelView( ModelView ):
    def is_accessible(self):
        return True


admin = Admin(app, url='/blog/admin')

admin.add_view(MyModelView(Category, db.session))
admin.add_view(MyModelView(Tag, db.session))
admin.add_view(MyModelView(Article, db.session))
admin.add_view(MyModelView(Comment, db.session))
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Link, db.session))
admin.add_view(MyModelView(BlackList, db.session))
admin.add_view(MyModelView(Subscriber, db.session))
