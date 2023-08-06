# coding: utf-8

from json import dumps, loads

import cherrypy
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from turbogears import controllers, database, expose, redirect, view
from turbogears.testutil import make_app, start_server, stop_server

import pytest


session = database.session

engine = database.get_engine()
metadata = database.get_metadata()

Base = declarative_base(bind=engine, metadata=metadata)


class User(Base):
    __tablename__ = 'test_user'

    id = sa.Column(sa.Integer, primary_key=True)
    user_name = sa.Column(sa.Unicode, nullable=False)


metadata.create_all(engine)


class Root(controllers.RootController):
    @expose()
    def index(self):
        return {}

    @expose()
    def users(self, user_name):
        user = User(user_name=user_name)
        session.add(user)

        return {'user_name': user.user_name}

    @expose()
    def should_rollback(self):
        user = User(user_name='phantom')
        session.add(user)
        session.flush()

        1/0

    @expose()
    def create_then_raise_redirect(self):
        user = User(user_name='dont_lose_me')
        session.add(user)
        session.flush()

        raise redirect('/')


    @expose()
    def create_then_raise_internal_redirect(self):
        user = User(user_name='███████████')
        session.add(user)
        session.flush()

        raise cherrypy.InternalRedirect('/')


@pytest.fixture
def app():
    return make_app(Root)


def test_users_endpoint_should_add_user(app):
    response = app.post('/users/newbie')

    assert session.query(User).filter_by(user_name='newbie').one()


def test_exception_endpoint_should_raise(app):
    app.get('/should_rollback', status=500)

    assert not session.query(User).filter_by(user_name='phantom').first()


def test_raise_redirect_should_commit_transaction(app):
    response = app.post('/create_then_raise_redirect')

    assert session.query(User).filter_by(user_name='dont_lose_me').one()


@pytest.mark.xfail('sys.version_info < (3,0)')
def test_raise_internal_redirect_should_commit_transaction(app):
    response = app.post('/create_then_raise_internal_redirect')

    assert session.query(User).filter_by(user_name='███████████').one()
