# tests

from warnings import filterwarnings, simplefilter, resetwarnings


def setup():
    # Ignore warning about missing NameMapper extension for cheetah
    filterwarnings('ignore', r'\n?.*\bNameMapper\b', UserWarning, 'cheetah')
    # DeprecationWarnings are ignored in Python 2.7 by default,
    # so add a filter that always shows them during the tests.
    simplefilter('always', DeprecationWarning)


def teardown():
    resetwarnings()
