#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import sys
from os import path

for p in ('../third-party', '..'):
    sys.path.insert(0, path.join(path.dirname(path.abspath(__file__)), p))

import cfg
import mage
import app
from mage import sqla


if __name__ == '__main__':
    mage.manage(dict(
        app=mage.application(app.app.as_wsgi(), namespace=dict(
                            db=app.session_maker(),
                        )),
        db=sqla.Commands(cfg.DATABASES, 
                         engine_params=cfg.DATABASE_PARAMS),
    ), sys.argv)
