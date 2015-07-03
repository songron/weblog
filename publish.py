#!/usr/bin/env python
#coding=utf8

""" A simple script for summitting articles written
in markdown.
"""


import argparse
import json
from StringIO import StringIO
import requests
import yaml


def get_file(path):
    if (path.startswith('http://') or path.startswith('https://') or
        path.startswith('ftp://')):
        r = requests.get(path)
        return StringIO(r.content)
    return open(path)


def publish(stream, api):
    """ Publishing a new article from `stream`"""

    headers = []
    for line in stream:
        line = line.rstrip()
        if not line:
            break
        headers.append(line)

    cfg = yaml.load(StringIO('\n'.join(headers)))
    if not cfg:
        raise ValueError('no valid yaml config informations')
    if 'title' not in cfg:
        raise ValueError('no title found')
    if 'tags' in cfg and not isinstance(cfg['tags'], list):
        raise ValueError('invalid tags: it should be list')

    bodies = []
    for line in stream:
        bodies.append(line.rstrip())
    content = '\n'.join(bodies).strip().decode('utf8')
    if not content:
        raise ValueError('no content found')

    data = {
        'title': cfg['title'],
        'summary': cfg.get('summary', None) or cfg['title'],
        'content': content,
    }
    if 'tags' in cfg:
        data['tags'] = cfg['tags']
    if 'pub_time' in cfg:
        data['pub_time'] = cfg['pub_time']

    r = requests.post(api, data=data)
    assert r.status_code == 200, r.content


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', help='markdown file path/url')
    parser.add_argument('-a', '--api', help='api address')
    args = parser.parse_args()

    if not args.path or not args.api:
        parser.print_help()
        return

    stream = get_file(args.path)
    publish(stream, args.api)


if __name__ == '__main__':
    main()
