#coding=utf8

import json
from flask import render_template, request, abort
from . import app
from .models import (Article, Tag, create_article)
from .utils import markdown2html, load_content


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
    content = load_content('about')
    return render_template('about.html',
                           content=content)


@app.route('/links')
def links():
    content = load_content('links')
    return render_template('links.html',
                           content=content)


@app.route('/publish', methods=['POST'])
def publish():
    title = request.form.get('title', None)
    if not title:
        return 'No title found', 500
    content = request.form.get('content', None)
    if not content:
        return 'No content found', 500
    pub_time = request.form.get('pub_time', None)
    tags = request.form.getlist('tags')

    create_article(title, content, pub_time, tags)
    return '', 200
