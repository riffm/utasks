# -*- coding: utf-8 -*-

from insanities import web
from insanities.forms import *
from models import Issue, Project, Comment


class IssueForm(Form):
    fields = [
        Field('issue', convs.Char(), widget=widgets.Textarea),
    ]


def get(env, data, nxt):
    issue = env.db.get(Issue, id=data.issue)
    if issue:
        data.issue = issue
        return nxt(env, data)
    return web.Response(status=404)


def create(env, data, nxt):
    data.form = form = IssueForm(env)
    db = env.db
    if env.request.method == 'POST':
        if form.accept(env.request.POST):
            text = form.python_data['issue']
            title, body = text, ''
            chunks = text.split('\r\n\r\n', 1)
            if len(chunks) > 1:
                title, body = chunks
            issue = Issue(title=title, proj=data.project)
            db.add(issue)
            if body:
                comment = Comment(issue=issue, raw=body, html=body)
                db.add(comment)
            db.commit()
            return env.redirect_to('issue', issue=issue.id)
    data.env = env
    return env.template.render_to_response('create-issue', data.as_dict())


def update(env, data, nxt):
    return nxt(env, data)
