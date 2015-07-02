#coding=utf8

from datetime import datetime
from .database import db


articles_tags = db.Table(
    'articles_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
    db.Column('article_id', db.Integer, db.ForeignKey('articles.id')))


class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    pub_time = db.Column(db.DateTime, default=datetime.now)
    tags = db.relationship('Tag',
                           secondary=articles_tags,
                           backref=db.backref('articles', lazy='dynamic'))

    def __init__(self, title, content, pub_time=None):
        self.title = title
        self.content = content
        if pub_time:
            self.pub_time = pub_time

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __init__(self, name):
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self


def _get_tag(name):
    tag = db.session.query(Tag).filter(Tag.name==name).first()
    if not tag:
        tag = Tag(name)
        tag.save()
    return tag


def create_article(title, content, pub_time=None, tagnames=[]):
    article = Article(title, content, pub_time)
    for tagname in tagnames:
        tag = _get_tag(tagname)
        article.tags.append(tag)
    article.save()
    return article
