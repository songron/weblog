WeBlog
======

A simple blog system based on [Flask](http://flask.pocoo.org/)


Quick Start
-----------

````
$ git clone https://github.com/ghostrong/weblog.git
$ cd weblog
$ pip install -r requirements.txt
$ python run.py
````

Now, visit `http://127.0.0.1:8888` in a browser.

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

````
$ python publish.py -a http://127.0.0.1:8888/publish -p example.md
````


Features
--------
* Writing blogs in Markdown and YAML
* Browsing blogs by PAGE or TAG
* Neat templates :-)
* Search (TBD)


TODO
----
* Keyword-based Search
