# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String
from sqlalchemy.schema import MetaData
from sqlalchemy.ext.declarative import declarative_base

from mage.sqla import *
from insanities.ext.auth import encrypt_password, check_password

metadata = MetaData()

MapedObject = declarative_base(metadata=metadata, name='MapedObject')



class User(MapedObject):
    __tablename__='user'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, default='')
    login = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.login)

    def set_password(self, password):
        self.password = encrypt_password(password)

    def check_password(self, password):
        return check_password(password, self.password)

    @classmethod
    def by_credential(cls, env, login, password):
        user = env.db.get(cls, login=login)
        if user and check_password(password, user.password):
            return user.id, None
        return None, u'Неправильный логин или пароль'

    @classmethod
    def by_id(cls, env, user_id):
        return env.db.get(cls, id=user_id)
