#coding=utf8

import sys
import os
abspath = os.path.abspath(__file__)
app_root = os.path.dirname(abspath)
path = os.path.join(app_root, 'virtualenv.bundle')
sys.path.insert(0, path)
sys.path.insert(0, app_root)

from flask import Flask
app = Flask(__name__)
app.config.from_object('config')
from views import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)
