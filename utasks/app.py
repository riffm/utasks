# -*- coding: utf-8 -*-

import memcache
from mage import sqla
from insanities import web
from insanities.templates import Template, mint
from insanities.ext.auth import CookieAuth

import cfg
import issue
import project
import user
import views
from models import User

session_maker = sqla.construct_maker(cfg.DATABASES, 
                                     engine_params=cfg.DATABASE_PARAMS)
template = Template(*cfg.TEMPLATES, engines={'mint': mint.TemplateEngine})
static = web.static_files(cfg.STATIC)
memcached = memcache.Client(cfg.MEMCACHE)
auth = CookieAuth(User.by_credential, User.by_id, 
                  memcached, cookie_name='utask-auth')


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
    auth.login_handler | template.render_to('login'),
    auth.logout_handler,

    auth | web.cases(
        web.match('/', 'dashboard') | views.dashboard,

        web.prefix('/issue') | web.cases(
            web.match('/<int:issue>', 'issue') | issue.get | web.cases(
                web.method('get'),
                web.method('post') | auth.login_required | issue.update,
                ) | template.render_to('issue'),
            ),

        web.prefix('/proj') | web.cases(
            web.match('', 'create-project') | auth.login_required | project.create,
            web.prefix('/<int:proj>') | project.get | web.cases(
                web.match('', 'project') | web.cases(
                    web.method('get'),
                    web.method('post') | project.update,
                    ) | template.render_to('proj'),
                web.match('/issue', 'create-issue') | issue.create,
                )
            ),

        web.prefix('/user') | web.cases(
            web.match('', 'create-user') | auth.login_required | user.create,
            web.match('/<int:user_id>', 'user') | user.get | web.cases(
                web.method('get'),
                web.method('post') | auth.login_required | user.update,
                ) | template.render_to('user'),
            )

        )
    )


url_for = web.Reverse.from_handler(app)
