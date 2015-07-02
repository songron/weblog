#coding=utf8

from flask import render_template
from . import app
from .models import (
    Article,
    Tag,
    get_tag,
    create_article
)
from .utils import markdown2html, load_aboutme


@app.route('/')
def index():
    pagination = Article.query.order_by(Article.id.desc()).paginate(1)
    return render_template('index.html',
                           pagination=pagination)


@app.route('/article/<id>')
def show_article(id):
    article = Article.query.get_or_404(id)
    return render_template('article.html',
                           entry=article)

@app.route('/tags')
def show_tags():
    tags = Tag.query.all()
    return render_template('tags.html',
                           tags=tags)

@app.route('/tag/<id>')
def show_tag(id):
    tag = Tag.query.get_or_404(id)
    articles = tag.articles.all()
    return render_template('tag.html',
                           tag=tag,
                           entries=articles)


@app.route('/about')
def about():
    content = load_aboutme()
    return render_template('about.html',
                           content=content)
