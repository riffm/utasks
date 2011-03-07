# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy import Table, UniqueConstraint
from sqlalchemy.orm import relation
from sqlalchemy.schema import MetaData
from sqlalchemy.ext.declarative import declarative_base

from mage.sqla import *
from insanities.ext.auth import encrypt_password, check_password

metadata = MetaData()

MapedObject = declarative_base(metadata=metadata, name='MapedObject')



class User(MapedObject):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, default='')
    login = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    projects = relation('Project', secondary='users_projects', backref='users')

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.login)

    def __repr__(self):
        return self.email.encode('utf-8')

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


class Project(MapedObject):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(String(1000))


users_projects = Table('users_projects', metadata, 
    Column('user_id', ForeignKey(User.id), nullable=False),
    Column('proj_id', ForeignKey(Project.id), nullable=False),
    UniqueConstraint('user_id', 'proj_id')
)


class Issue(MapedObject):
    __tablename__ = 'issue'
    OPEN = 0
    DONE = 1
    CLOSED = 2
    REOPEN = 3
    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    proj_id = Column(Integer, ForeignKey(Project.id), nullable=False)
    proj = relation(Project, backref='issues')
    state = Column(Integer, nullable=False, default=OPEN)


class Comment(MapedObject):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    issue_id = Column(Integer, ForeignKey(Issue.id), nullable=False)
    issue = relation(Issue, backref='comments')
    raw = Column(String(1000), nullable=False)
    html = Column(String(1000), nullable=False)
