#coding=utf8

import markdown
from datetime import datetime
from . import app


def format_date(dateobj):
    return dateobj.strftime(
        '%b %d,%Y')


def format_date_weekday(dateobj):
    return dateobj.strftime(
        '%A %b %d,%Y')


def format_datetime(dateobj):
    return dateobj.strftime(
        '%A %b %d,%Y %H:%M:%S')


app.jinja_env.globals['format_date'] = format_date
app.jinja_env.globals['format_date_weekday'] = format_date_weekday
app.jinja_env.globals['format_datetime'] = format_datetime


def markdown2html(mdtext):
    return markdown.markdown(mdtext)

def load_content(name):
    with open('{}.md'.format(name)) as f:
        mdtext = f.read().decode('utf8', 'ignore')
    return markdown2html(mdtext)
