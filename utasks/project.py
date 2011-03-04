# -*- coding: utf-8 -*-

from insanities import web
from models import Project


def get(env, data, nxt):
    proj = env.db.get(Project, name=data.project)
    if proj:
        data.project = proj
        return nxt(env, data)
    return web.Response(status=404)


def create(env, data, nxt):
    return nxt(env, data)


def update(env, data, nxt):
    return nxt(env, data)
