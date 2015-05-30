#coding=utf8

from datetime import datetime
from . import app
from .database import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __unicode__(self):
        return self.name


article_tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('article_id', db.Integer, db.ForeignKey('article.id')),
)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __unicode__(self):
        return self.name


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    status = db.Column(db.Integer, default=1) # 0:Draft, 1:Finished, -1:Invalid
    created_time = db.Column(db.DateTime, default=datetime.now)
    modified_time = db.Column(db.DateTime, default=datetime.now)
    is_always_above = db.Column(db.Integer, default=0) # top
    share = db.Column(db.Integer, default=0) # share to social networks
    click_count = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('articles',lazy='dynamic'), lazy='select')
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), default=1)
    author = db.relationship('User', backref='articles', lazy='select')
    tags = db.relationship('Tag', secondary=article_tags, backref=db.backref('articles',lazy='dynamic'))

    def __unicode__(self):
        return self.title


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email_address = db.Column(db.String(80))
    site = db.Column(db.String(100))
    avatar = db.Column(db.String(100))
    content = db.Column(db.Text)
    post_date = db.Column(db.DateTime, default=datetime.now)
    visible = db.Column(db.Integer, default=1)
    ip = db.Column(db.String(15))
    reply_to_comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    reply_to_comment = db.relationship('Comment', backref='comments', remote_side=[id])
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    article = db.relationship('Article', backref=db.backref('comments',lazy='dynamic'))

    def __unicode__(self):
        return self.content


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.BigInteger)
    name = db.Column(db.String(50))
    avatar = db.Column(db.String(100))
    token = db.Column(db.String(80))
    login_type = db.Column(db.Integer) #1:weibo;

    def __unicode__(self):
        return self.name


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    site = db.Column(db.String(100)) #url

    def __unicode__(self):
        return self.name


class BlackList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(15))

    def __unicode__(self):
        return self.ip_address


class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email_address = db.Column(db.String(80))
    subscrible_time = db.Column(db.DateTime, default=datetime.now)
    enabled = db.Column(db.Integer, default=True)

    def __unicode__(self):
        return self.username
