eBlog
======

A simple blog system based on [Flask](http://flask.pocoo.org/)

其他网站推荐 Recommendations
=====

[木兰词](https://www.mulanci.org/)：中文歌词网站

[初心阅读](https://www.bemind.site/)： 中文短篇阅读推荐

[Vinyl World](https://www.vinylworld.org/)： 关于黑胶唱片、唱片店的爱好者网站


Quick Start
-----------

````
$ git clone https://github.com/ghostrong/weblog.git
$ cd weblog
$ pip install -r requirements.txt
$ python create_db.py
$ python run.py (also you can run shell with: sh start.sh)
````

Now, visit `http://127.0.0.1:5000` in a browser.

Database with MySQL
-------------------
If you use MySQL ,create weblog database before ```python create_db.py```:

* Set **SQLALCHEMY_DATABASE_URI** in config.py
* Login MySQL and execute script ```create schema weblog charset utf8;```
* python create_db.py

Requirements
------------

#### For the server-side

* Flask
* Flask-SQLAlchemy
* itsdangerous
* Jinja2
* Markdown
* MarkupSafe
* SQLAlchemy
* Werkzeug

#### For the cline-side (for publishing articles automatically)

* requests
* lxml
* PyYAML
* Markdown


Writing blogs
-------------

You should write articles in [markdown](http://daringfireball.net/projects/markdown/), and provide the meta information such as title, tags in [YAML](http://yaml.org/). You should put the meta data in the header lines of the markdown file. Here is an [example](https://raw.githubusercontent.com/ghostrong/weblog/master/example.md).

#### Meta Data

* **title**

  You must give the title the the blog. e.g.,

  ````
  title: The Zen of Python
  ````

* **summary** (optional)

  It's the abstract of the article. If you ignore it, the publish helper will generate the
  summary snippet from the body automatically. e.g.,

  ````
  summary:
    Long time Pythoneer Tim Peters succinctly channels the BDFL's
    guiding principles for Python's design into 20 aphorisms, only 19
    of which have been written down.
  ````

* **pub_time** (optional)

  You can define the publish datetime manually. Or, the system will assign the current
  datetime. The default format is "%Y-%m-%d %H:%M:%S" (such as "2015-06-06 12:40:10").
  You could define the time string format by the value of *TIME_FORMAT* in
  [config.py](config.py),
  and you should conform to the
  [format codes](https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior). e.g.,

  ````
  pub_time: 2015-06-06 12:40:10
  ````

* **tags** (optional)

  It's useful to assign tags to an article. The value type should be list in YAML. e.g.,

  ````
  tags:
    - python
    - programming
  ````

#### The boundry of meta

The meta data should be located between '---' and '...'.
The following is an example of meta infomration:

````
---
title: The Zen of Python
summary:
  Long time Pythoneer Tim Peters succinctly channels the BDFL's
  guiding principles for Python's design into 20 aphorisms, only 19
  of which have been written down.
tags:
  - python
  - programming
...

You should write the body content from here...
````


Publishing blogs
----------------

We provide a simple script to make the publishing work easy. Run `publish.py` to check the help message.

````
$ python publish

usage: publish.py [-h] [-p PATH] [-a API] [-t TOKEN]

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  markdown file path/url
  -a API, --api API     api address
  -t TOKEN, --token TOKEN
                        access token
````

You should provide the markdown file(either file-path or raw-url), the target api, and the access token. In this blog system, the publish url is `/publish`. The access token is the value of *TOKEN* in [config.py](config.py). 
**Anyone who know the token could publish articles to your blog system, so keep it secret!!**

After starting the web server locally, you can publish an article like this:
*You should be change your token in config.py file.

````
$ python publish.py -a http://127.0.0.1:5000/publish -p example.md -t your_token_in_config
````

Deploy application
------------------
gunicorn -w 4 -b 0.0.0.0:5000 run:app

Delete blogs
------------
```
from weblog import database,models
db = database.db
articles=models.Article
articles.query.filter_by(id=1).delete()
db.session.commit()
```
Features
--------
* Writing blogs in Markdown and YAML
* Browsing blogs by PAGE or TAG
* Neat templates :-)
* Search (TBD)


TODO
----
* Keyword-based Search
