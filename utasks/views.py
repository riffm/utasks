# -*- coding: utf-8 -*-

from insanities import web
from models import Issue


def dashboard(env, data, nxt):
    data.issues = env.db.query(Issue)
    data.env = env
    return env.template.render_to_response('dashboard', data.as_dict())
