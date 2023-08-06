import logging

import cherrypy
from cherrypy import request
import sqlalchemy, sqlalchemy.orm
from sqlalchemy import MetaData
from sqlalchemy.exc import ArgumentError, OperationalError
from turbogears import config

from . import DatabaseConfigurationError


log = logging.getLogger('turbogears.database')


_metadatas = {}
_metadatas[None] = MetaData()
metadata = _metadatas[None]


def get_engine(pkg=None):
    """Retrieve the engine based on the current configuration."""

    bind_metadata()

    return get_metadata(pkg).bind


def get_metadata(pkg=None):
    """Retrieve the metadata for the specified package."""

    try:
        return _metadatas[pkg]
    except KeyError:
        _metadatas[pkg] = MetaData()

        return _metadatas[pkg]


def bind_metadata():
    """Connect SQLAlchemy to the configured database(s)."""
    if metadata.is_bound():
        return

    alch_args = dict()
    for k, v in list(config.items()):
        if 'sqlalchemy' in k:
            alch_args[k.split('.', 1)[-1]] = v

    try:
        dburi = alch_args.pop('dburi')
        metadata.bind = sqlalchemy.create_engine(dburi, **alch_args)
    except KeyError:
        raise DatabaseConfigurationError(
            "No sqlalchemy database configuration found!")
    except ArgumentError as exc:
        raise DatabaseConfigurationError(exc)

    for k, v in list(config.items()):
        if '.dburi' in k and 'sqlalchemy.' not in k:
            get_metadata(k.split('.', 1)[0]
                ).bind = sqlalchemy.create_engine(v, **alch_args)


def create_session():
    """Create a session that uses the engine from thread-local metadata.

    The session by default does not begin a transaction, and requires that
    flush() be called explicitly in order to persist results to the database.

    """
    if not metadata.is_bound():
        bind_metadata()
    return sqlalchemy.orm.create_session()


session = sqlalchemy.orm.scoped_session(create_session)


# Note: TurboGears used to set mapper = Session.mapper, but this has
# been deprecated in SQLAlchemy 0.5.5. If it is unavailable, we emulate
# the behaviour of the old session-aware mapper following this recipe
# from the SQLAlchemy wiki:
#
# http://www.sqlalchemy.org/trac/wiki/UsageRecipes/SessionAwareMapper
#
# If you do not want to use the session-aware mapper, import 'mapper'
# directly from sqlalchemy.orm. See model.py in the default quickstart
# template for an example.
def create_session_mapper(scoped_session=session):
    def mapper(cls, *args, **kw):
        set_kwargs_on_init = kw.pop('set_kwargs_on_init', True)
        validate = kw.pop('validate', False)
        # we accept 'save_on_init' as an alias for 'autoadd' for backward
        # compatibility, but 'autoadd' is shorter and more to the point.
        autoadd = kw.pop('autoadd', kw.pop('save_on_init', True))

        if set_kwargs_on_init and (getattr(cls,
                    '__init__', object.__init__) is object.__init__
                or getattr(cls.__init__, '_session_mapper', False)):
            def __init__(self, **kwargs):
                for key, value in list(kwargs.items()):
                    if validate:
                        if not hasattr(self, key):
                            raise TypeError(
                                "Invalid __init__ argument: '%s'" % key)
                    setattr(self, key, value)
                if autoadd:
                    session.add(self)
            __init__._session_mapper = True
            cls.__init__ = __init__
        cls.query = scoped_session.query_property()
        return sqlalchemy.orm.mapper(cls, *args, **kw)
    return mapper


session_mapper = create_session_mapper()
mapper = session_mapper


def run_with_transaction(func, *args, **kw):
    log.debug("Starting SA transaction")
    request.sa_transaction = session.begin()
    try:
        try:
            retval = func(*args, **kw)
        except (cherrypy.HTTPRedirect, cherrypy.InternalRedirect):
            # If a redirect happens, commit and proceed with redirect.
            if sa_transaction_active():
                log.debug('Redirect in active transaction - will commit now')
                session.commit()
            else:
                log.debug('Redirect in inactive transaction')
            raise
        except:
            # If any other exception happens, rollback and re-raise error
            if sa_transaction_active():
                log.debug('Error in active transaction - will rollback now')
                session.rollback()
            else:
                log.debug('Error in inactive transaction')
            raise
        # If the call was successful, commit and proceed
        if sa_transaction_active():
            log.debug('Transaction is still active - will commit now')
            session.commit()
        else:
            log.debug('Transaction is already inactive')
    finally:
        log.debug('Ending SA transaction')
        session.close()
    return retval


def restart_transaction(args):
    log.debug("Restarting SA transaction")
    if sa_transaction_active():
        log.debug('Transaction is still active - will rollback now')
        session.rollback()
    else:
        log.debug('Transaction is already inactive')
    session.close()
    request.sa_transaction = session.begin()


def sa_transaction_active():
    """Check whether SA transaction is still active."""
    try:
        return session.is_active
    except AttributeError: # SA < 0.4.9
        try:
            return session().is_active
        except (TypeError, AttributeError): # SA < 0.4.7
            try:
                transaction = request.sa_transaction
                return transaction and transaction.is_active
            except AttributeError:
                return False


def EndTransactions():
    session.expunge_all()
