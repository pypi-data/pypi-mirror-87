from functools import wraps


def wraps_exposed(fn):
    def wrap_decorator(wrapper_fn):
        wrapper_fn = wraps(fn)(wrapper_fn)

        if getattr(fn, 'exposed', False):
            wrapper_fn.exposed = True

        # Preserve cherrypy.tool decorators and other function-level
        # configuration
        try:
            wrapper_fn._cp_config = fn._cp_config.copy()
        except AttributeError:
            pass

        return wrapper_fn

    return wrap_decorator
