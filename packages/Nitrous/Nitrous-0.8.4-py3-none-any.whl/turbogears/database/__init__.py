"""Convenient access to an SQLAlchemy managed database."""

__all__ = ['bind_metadata', 'create_session', 'DatabaseError',
    'DatabaseConfigurationError', 'EndTransactions', 'get_engine',
    'get_metadata', 'mapper', 'metadata', 'session', 'session_mapper',
    'set_db_uri']


import sys
import logging

from turbogears import config
from turbogears.util import remove_keys

log = logging.getLogger('turbogears.database')


try:
    import sqlalchemy
except ImportError:
    log.warning('SQLAlchemy not installed; database features disabled.')

    sqlalchemy = None


class DatabaseError(Exception):
    """TurboGears Database Error."""


class DatabaseConfigurationError(DatabaseError):
    """TurboGears Database Configuration Error."""


if sqlalchemy:
    from .sqlalchemy_support import get_engine, get_metadata, bind_metadata, \
        create_session, run_with_transaction, restart_transaction, \
        EndTransactions, session, metadata, mapper
else:
    def get_engine(pkg=None):
        pass
    def get_metadata(pkg=None):
        pass
    def bind_metadata():
        pass
    def create_session():
        pass
    def run_with_transaction(func, *args, **kw):
        pass
    def restart_transaction(args):
        pass
    def EndTransactions():
        pass
    session = metadata = mapper = None


def set_db_uri(dburi, package=None):
    """Set the database URI.

    Sets the database URI to use either globally or for a specific package.
    Note that once the database is accessed, calling it will have no effect.

    @param dburi: database URI to use
    @param package: package name this applies to, or None to set the default.

    """
    if package:
        config.update({'%s.dburi' % package: dburi})
    else:
        config.update({'sqlalchemy.dburi': dburi})


def dispatch_exception(exception, args, kw):
    # errorhandling import here to avoid circular imports
    from turbogears.errorhandling import dispatch_error

    # Keep in mind func is not the real func but _expose
    real_func, accept, allow_json, controller = args[:4]
    args = args[4:]
    exc_type, exc_value, exc_trace = sys.exc_info()
    remove_keys(kw, ('tg_source', 'tg_errors', 'tg_exceptions'))

    return dispatch_error(
            controller, real_func, None, exception, *args, **kw)
