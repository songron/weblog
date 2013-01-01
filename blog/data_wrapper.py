#coding=utf8

from data import *
from sqlalchemy import and_, or_
from sqlalchemy.sql import func

class DataWrapper(object):
    def get_all_category(self):
        return Category.query.all()

    def get_all_tag(self):
        return Tag.query.all()

    def create_article(self, title, content, tags, category):
        a = Article(title=title, content=content, category_id=category)
        tag_list = tags.split()
        for name in tag_list:
            #不需要lower限制，默认就是忽略大小写的
            #t = db.session.query(Tag).filter( func.lower(Tag.name)==name.lower() ).first()
            t = db.session.query(Tag).filter( Tag.name==name ).first()
            if not t:
                t = Tag(name=name)
            a.tags.append(t)
        db.session.add(a)
        db.session.commit()
        return a

    def get_article_by_id(self, id):
        article = Article.query.get(id)
        return article

    def get_article_by_page(self, pid, per_page):
        p = Article.query.order_by(Article.created_time.desc()).paginate(pid, per_page)
        return p

    def search_article(self, keywords, page=1, per_page=10):
        filter_clause = []
        for k in keywords.split():
            filter_clause.append( or_(*[ Article.title.contains(k),
                                        Article.content.contains(k)]) )
        articles = Article.query.filter( and_(*filter_clause) ).all()
        return articles

    def get_category_by_id(self, id):
        return Category.query.get(id)

    def get_tag_by_id(self, id):
        return Tag.query.get(id)

    def create_comment(self, username, email_address, site, avatar, content, ip, \
                        reply_to_comment_id, article_id):
        c = Comment(username=username, email_address=email_address, site=site, \
            avatar=avatar, content=content, ip=ip, article_id=article_id)
        if reply_to_comment_id:
            c.reply_to_comment_id = int(reply_to_comment_id)
        db.session.add(c)
        db.session.commit()
        return c

    def get_comment_by_id(self, id):
        comment = Comment.query.get(id)
        return comment

    def get_user_by_id(self, id):
        user = User.query.get(id)
        return user

    def get_all_link(self):
        links = Link.query.all()
        return links


if __name__ == '__main__':
    pass
