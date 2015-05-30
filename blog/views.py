#coding=utf8

from datetime import datetime
import time
import json
from StringIO import StringIO
from werkzeug import secure_filename
from flask import (Blueprint, request, render_template, redirect, g, url_for,
                   abort)
from html2text import html2text

from . import app
# from data import *
# from blog.admin import *  #
# from blog.data_wrapper import DataWrapper
# dw = DataWrapper()
#blog = Blueprint('blog', __name__,
#    template_folder='templates',
#    )

def _timestr0(dt):
    mon = Mons[str(dt.month)]
    return u'%s月<span>%d</span>' % (mon, dt.day)
app.jinja_env.filters['timestr0'] = _timestr0

def _timestr1(dt):
    return '%d:%d' % ( dt.hour, dt.minute )
app.jinja_env.filters['timestr1'] = _timestr1

def _timestr2(dt):
    return u'%d年%d月%d日 %d:%d:%d' % ( dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second )
app.jinja_env.filters['timestr2'] = _timestr2

def _html2text(html):
    sio = StringIO()
    html2text.html2text_file(html, sio.write)
    text = sio.getvalue()
    sio.close()
    return text
app.jinja_env.filters['html2text'] = _html2text


@app.before_request
def before_request():
    g.user = app.config['USER']


def _global_maps():
    categories = dw.get_all_category()
    links = dw.get_all_link()
    maps = {
        'categories': categories,
        'links': links,
    }
    return maps


@app.route('/')
@app.route('/page/<int:pid>')
def index(pid=1):
    per_page = 10
    p = dw.get_article_by_page(pid, per_page)
    articles = p.items
    if not p.total:
        pagination = [0]
    elif p.total % per_page:
        pagination = range( 1, p.total/per_page + 2 )
    else:
        pagination = range( 1, p.total/per_page + 1 )

    return render_template('blog/index.html',
        articles=articles,
        pid=pid,
        pagination=pagination[:10],
        last_page = pagination[-1],
        nav_current="index",
        **_global_maps()
        )


@app.route('/category/')
@app.route('/category/<int:cid>')
def category(cid=0):
    if cid != 0:
        return redirect( url_for('.search',category=cid) )
    return render_template('blog/category.html',
        nav_current="category",
        **_global_maps()
        )


@app.route('/contact/')
def contact():
    article = dw.get_article_by_id(1) #id=1, the default article
    if not article:
        dw.create_article('default', 'default', '', None)
        article = dw.get_article_by_id(1) #id=1, the default article
    comments = article.comments.order_by(Comment.post_date).all() #升序排序
    return render_template('blog/contact.html',
        article=article,
        comments=comments,
        nav_current="contact",
        **_global_maps()
        )


@app.route('/about/')
def about():
    return render_template('blog/about.html',
        nav_current="about",
        **_global_maps()
        )


@app.route('/article/<int:id>')
def article(id):
    article = dw.get_article_by_id(id)
    if not article:
        abort(404)
        #return '404'
    comments = article.comments.order_by(Comment.post_date).all() #升序排序
    return render_template('blog/article.html',
        article=article,
        comments=comments,
        **_global_maps()
        )


@app.route('/new_comment', methods=['POST'])
def new_comment():
    username = request.form.get('username', '')
    avatar = request.form.get('avatar', '')
    email_address = request.form.get('email_address', '')
    site = request.form.get('site', '')
    content = request.form.get('content', '')
    ip = request.environ['REMOTE_ADDR']

    article_id = request.form.get('article', None)
    reply_to_comment_id = request.form.get('reply_to_comment', None)

    c = dw.create_comment(username, email_address, site, avatar, content, ip, \
                        reply_to_comment_id, int(article_id))
    avatar = c.avatar
    if not avatar:
        avatar = '/static/blog/coolblue/images/gravatar.jpg'
    if c.reply_to_comment:
        reply_to = c.reply_to_comment.username
        reply_link = '#comment-%d' % c.reply_to_comment.id
    else:
        reply_to = g.user['name']
        reply_link = '#article-%d' % c.article.id
    maps = {
        'id': c.id,
        'username': c.username,
        'content': c.content,
        'timestr2': _timestr2(c.post_date),
        'avatar': avatar,
        'reply_to': reply_to,
        'reply_link': reply_link,
    }
    res = u'''
<li id="comment-%(id)d" class="depth-1 newest">
	<div class="comment-info">
	    <img alt="头像" src="%(avatar)s" class="avatar" height="40" width="40" />
			<cite>
				<a href="#comment-%(id)d" onclick="return false;">%(username)s</a>
                回复<a href="%(reply_link)s">@%(reply_to)s</a>
                ： <br />
				<span class="comment-data">
                    <a href="#comment-%(id)d" title="" onclick="return false;">%(timestr2)s</a>
                </span>
			</cite>
	</div>
	<div class="comment-text">
		<p>%(content)s</p>
		<div class="reply">
			<a rel="nofollow" class="comment-reply-link" href="#comment-%(id)d"
               name="回复%(username)s：">回复</a>
 		</div>
	</div>
</li>
    ''' % maps
    return res


@app.route('/tag/<int:tid>')
def tag(tid):
    return redirect( url_for('.search',tag=tid) )


@app.route('/search/')
def search():
    category_id = request.args.get('category','')
    tag_id = request.args.get('tag', '')
    category = ''
    tag = ''
    if category_id:
        category_id = int(category_id)
        category = dw.get_category_by_id(category_id)
        if category:
            articles = category.articles.order_by(Article.created_time.desc()).all()
        else:
            articles = []
        search = 'category'
    elif tag_id:
        tag_id = int(tag_id)
        tag = dw.get_tag_by_id(tag_id)
        if tag:
            articles = tag.articles.order_by(Article.created_time.desc()).all()
        else:
            articles = []
        search = 'tag'
    else:
        #暂不分页, 很锉的一个搜索
        keywords = request.args.get('q', '')
        articles = dw.search_article(keywords)
        search = 'search' #标记是关键词搜索还是博客分类

    return render_template('blog/search_results.html',
        search=search,
        articles=articles,
        total = len(articles),
        category = category,
        tag=tag,
        **_global_maps()
    )


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    f = request.files.get('imgFile', None)
    if not f:
        data = {'error':1, 'message':'No File Found!'}
        return json.dumps(data)
    filename = str(int(time.time())) + '_' + secure_filename(f.filename)
    s = sae.storage.Client()
    ob = sae.storage.Object(f.read())
    s.put('upload', filename, ob)
    url = s.url('upload', filename)
    data = {'error':0, 'url':url}
    return json.dumps(data)
