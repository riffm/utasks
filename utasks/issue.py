# -*- coding: utf-8 -*-

from insanities import web
from insanities.forms import *
from models import Issue, Project, Comment, User
from utils import ModelChoice


class IssueForm(Form):
    fields = [
        Field('issue', convs.Char(), widget=widgets.Textarea),
        Field('deadline', convs.Date(format='%d/%m/%Y', required=False), label=u'срок'),
        Field('executor', ModelChoice(model=User, 
                                      get_object_label=lambda o: o.name), 
              widget=widgets.Select),
    ]


class CommentForm(Form):
    fields = [
        Field('comment', convs.Char(), widget=widgets.Textarea),
        Field('comment_and_close', convs.Bool(), default=False, 
              widget=widgets.HiddenInput),
    ]


def get(env, data, nxt):
    issue = env.db.get(Issue, id=data.issue)
    if issue:
        data.issue = issue
        data.form = CommentForm(env)
        return nxt(env, data)
    return web.Response(status=404)


def create(env, data, nxt):
    data.form = form = IssueForm(env)
    db = env.db
    if env.request.method == 'POST':
        if form.accept(env.request.POST):
            deadline = form.python_data['deadline']
            text = form.python_data['issue']
            title, body = text, ''
            chunks = text.split('\r\n\r\n', 1)
            if len(chunks) > 1:
                title, body = chunks
            issue = Issue(title=title, proj=data.project, 
                          author=env.user, deadline=deadline)
            issue.executor = form.python_data['executor']
            db.add(issue)
            if body:
                comment = Comment(issue=issue, raw=body, html=body, author=env.user)
                db.add(comment)
            db.commit()
            return env.redirect_to('issue', issue=issue.id)
    data.env = env
    return env.template.render_to_response('create-issue', data.as_dict())


def update(env, data, nxt):
    issue = data.issue
    data.form = form = CommentForm(env)
    if form.accept(env.request.POST):
        db = env.db
        text = form.python_data['comment']
        comment = Comment(raw=text, html=text, issue=issue, author=env.user)
        if form.python_data['comment_and_close']:
            issue.done = True
        db.add(comment)
        db.commit()
        return env.redirect_to('issue', issue=issue.id)
    data.env = env
    return nxt(env, data)
