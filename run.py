#!/usr/bin/env python
#coding=utf8

from weblog import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
