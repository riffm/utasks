# -*- coding: utf-8 -*-

from insanities import web
from insanities.forms import *
from models import Issue, Project, Comment, User
from utils import ModelChoice


class IssueForm(Form):
    fields = [
        Field('issue', convs.Char(), widget=widgets.Textarea),
        Field('executor', ModelChoice(model=User, 
                                      get_object_label=lambda o: o.name), 
              widget=widgets.Select),
    ]


class CommentForm(Form):
    states = (
        (Issue.OPEN, u'новая'),
        (Issue.DONE, u'сделана'),
        (Issue.CLOSED, u'закрыта'),
        (Issue.REOPEN, u'открыта заново'),
    )

    fields = [
        Field('comment', convs.Char(), widget=widgets.Textarea),
        Field('state', convs.EnumChoice(choices=states, conv=convs.Int()), 
              widget=widgets.HiddenInput),
    ]


def get(env, data, nxt):
    issue = env.db.get(Issue, id=data.issue)
    if issue:
        data.issue = issue
        data.form = CommentForm(env, initial={'state':issue.state})
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
            issue = Issue(title=title, proj=data.project, author=env.user)
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
    data.form = form = CommentForm(env, initial=dict(state=issue.state))
    if form.accept(env.request.POST):
        db = env.db
        text = form.python_data['comment']
        state = form.python_data['state']
        issue.state = state
        comment = Comment(raw=text, html=text, issue=issue, author=env.user)
        db.add(comment)
        db.commit()
        return env.redirect_to('issue', issue=issue.id)
    data.env = env
    return nxt(env, data)
