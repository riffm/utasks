# -*- coding: utf-8 -*-

import sys
from os import path

from insanities.templates import mint

cur_dir = path.abspath(path.dirname(path.abspath(__file__)))

def rel(*args):
    args = [cur_dir] + list(args)
    return path.join(*args)

LOG_FILE = rel('var', 'fcgi.log')

TEMPLATES = [rel('templates'), mint.TEMPLATE_DIR]

STATIC = rel('static')


DATABASES = {
    '':'sqlite:///:memory:',
}


DATABASE_PARAMS = {
    'pool_size': 10,
    'echo':True,
}


MEMCACHE = ['127.0.0.1:11211']


if path.exists(rel('cfg_local.py')):
    from cfg_local import *
