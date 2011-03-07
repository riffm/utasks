# -*- coding: utf-8 -*-

from models import User


def create_admin(db):
    admin = User()
    admin.name = admin.login = 'admin'
    admin.set_password('admin')
    admin.email = 'admin@local.local'
    db.add(admin)


def initial(db):
    create_admin(db)
    db.commit()
