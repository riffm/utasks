# -*- coding: utf-8 -*-

from insanities import web
from insanities.forms import *
from models import Project, User
from utils import ModelChoice


class ProjectForm(Form):
    fields = [
        Field('name', convs.Char(), label=u'Название'),
        Field('description', convs.Char(required=False), 
              label=u'Описание',
              widget=widgets.Textarea),
        Field('users', ModelChoice(model=User, 
                                   multiple=True,
                                   get_object_label=lambda o: o.name), 
              widget=widgets.Select),
    ]


def get(env, data, nxt):
    proj = env.db.get(Project, id=data.proj)
    if proj:
        data.project = proj
        return nxt(env, data)
    return web.Response(status=404)


def create(env, data, nxt):
    data.form = form = ProjectForm(env)
    if env.request.method == 'POST':
        if form.accept(env.request.POST):
            proj = Project(**form.python_data)
            env.user.projects = env.user.projects + [proj]
            env.db.add(proj)
            env.db.commit()
            return env.redirect_to('project', proj=proj.id)
    data.env = env
    return env.template.render_to_response('create-project', data.as_dict())


def update(env, data, nxt):
    proj = data.project
    if not env.user in proj.users:
        return web.Response(status=401)
    initial = {}
    for field in ProjectForm.fields:
        initial[field.name] = getattr(proj, field.name, None)
    data.form = form = ProjectForm(env, initial=initial)
    if env.request.method == 'POST':
        if form.accept(env.request.POST):
            for k, v in form.python_data.items():
                setattr(proj, k, v)
            env.db.commit()
            return env.redirect_to('project', proj=proj.id)
    data.env = env
    return env.template.render_to_response('update-project', data.as_dict())
