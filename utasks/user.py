# -*- coding: utf-8 -*-

from sqlalchemy.sql.expression import or_
from insanities import web
from insanities.forms import *
from models import Issue, Project, Comment, User

from utils import ModelChoice, PasswordSet


class UserForm(Form):
    fields = [
        Field('name', convs.Char(required=False), label=u'Имя'),
        Field('login', convs.Char(), label=u'login'),
        Field('email', convs.Char(), label=u'email'),
        PasswordSet(label=u'пароль'),
        Field('projects', ModelChoice(model=Project,
                                      multiple=True,
                                      get_object_label=lambda o: o.name),
              widget=widgets.Select),
    ]


def get(env, data, nxt):
    user = env.db.get(User, id=data.user_id)
    if user:
        data.user = user
        data.issues = env.db.query(Issue).filter(or_(Issue.author==user, 
                                                 Issue.executor==user))
        return nxt(env, data)
    return web.Response(status=404)


def create(env, data, nxt):
    data.form = form = UserForm(env)
    db = env.db
    if env.request.method == 'POST':
        if form.accept(env.request.POST):
            password = form.python_data.pop('password')
            user = User(**form.python_data)
            user.set_password(password)
            db.add(user)
            db.commit()
            return env.redirect_to('user', user_id=user.id)
    data.env = env
    return env.template.render_to_response('create-user', data.as_dict())


def update(env, data, nxt):
    return nxt(env, data)
