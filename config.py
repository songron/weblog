#coding=utf8

#DEBUG = True
FRAGMENT_PER_PAGE = 10

# -- Flask - SQLALCHEMY --
MYSQL_HOST = 'localhost'
MYSQL_PORT = '3306'
MYSQL_USER = ''
MYSQL_PASS = ''
MYSQL_DB = ''
SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s:%s/%s' % (MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT, MYSQL_DB)

USER = {
    'name': u'马孔多',
    'avatar': u'http://tp4.sinaimg.cn/1990786715/180/5642425207/1',
    'avatar_large': u'http://whoop-upload.stor.sinaapp.com/1353599241_me.jpg',
    'email': u'rongxiaosong@gmail.com',
    'weibo': u'http://weibo.com/rongxs',
    'intro': u'''
    马孔多，《百年孤独》的小镇，取这个名字并不代表我很文艺。正在读书的程序员，\
    每天十几个小时坐在电脑前会压抑人的神经，所以酷爱户外运动，爬山最佳。此外，\
    读书、电影也是必不可少。广招朋友，欢迎IT人士以及有各类爱好的朋友前来指教。\
    Feel Free to Email Me: rongxiaosong@gmail.com
    '''
}

Mons = {
    '1':u'一',
    '2':u'二',
    '3':u'三',
    '4':u'四',
    '5':u'五',
    '6':u'六',
    '7':u'七',
    '8':u'八',
    '9':u'九',
    '10':u'十',
    '11':u'十一',
    '12':u'十二'
}
