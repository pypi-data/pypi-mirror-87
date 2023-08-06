import cherrypy
from turbogears import config, view

import pytest


@pytest.fixture(autouse=True, scope='session')
def load_engines():
    view.load_engines()


@pytest.fixture(autouse=True, scope='session')
def update_config():
    config.update_config({'tg.empty_flash': False})


@pytest.fixture(autouse=True)
def clear_validation_state():
    """Ensure validators actually get run by deleting

        cherrypy.request.validation_state

    if defined."""

    try:
        del cherrypy.request.validation_state
    except AttributeError:
        pass
