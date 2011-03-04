# -*- coding: utf-8 -*-

import memcache
from mage import sqla
from insanities import web
from insanities.templates import Template, mint
from insanities.ext.auth import CookieAuth

import cfg
from models import User

session_maker = sqla.construct_maker(cfg.DATABASES, 
                                     engine_params=cfg.DATABASE_PARAMS)
template = Template(*cfg.TEMPLATES, engines={'mint': mint.TemplateEngine})
static = web.static_files(cfg.STATIC)
memcached = memcache.Client(cfg.MEMCACHE)
auth = CookieAuth(User.by_credential, User.by_id, 
                  memcached, cookie_name='di-auth')


def redirect_to(*args, **kwargs):
    response = web.Response(status=303)
    response.headers['Location'] = str(url_for(*args, **kwargs))
    return response


def config(env, data, next_handler):
    # template incapsulation
    env.template = template

    # make session object for each request
    env.db = session_maker()

    # reverse
    env.url_for = url_for

    # cache (session_storage is not good name)
    env.session_storage = memcached

    # why not to have url for static files?
    # useful in templates
    env.url_for_static = static.construct_reverse()

    # redirect shortcut
    env.redirect_to = redirect_to

    try:
        return next_handler(env, data)
    finally:
        env.db.close()


app = web.handler(config) | web.cases(
    static,
    web.match('/', 'index') | (lambda e,d,n: web.Response('hello'))
)


url_for = web.Reverse.from_handler(app)
