# -*- coding: utf-8 -*-

from insanities import web
from models import Issue, Project


def get(env, data, nxt):
    issue = env.db.get(Issue, id=data.issue)
    if issue:
        data.issue = issue
        return nxt(env, data)
    return web.Response(status=404)


def create(env, data, nxt):
    return nxt(env, data)


def update(env, data, nxt):
    return nxt(env, data)
