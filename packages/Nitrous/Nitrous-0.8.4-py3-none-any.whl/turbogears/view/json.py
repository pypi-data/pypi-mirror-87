from datetime import date, datetime
from uuid import UUID

from simplejson import dumps


def default(obj):
    if isinstance(obj, (date, datetime, UUID)):
        return str(obj)

    try:
        return obj.__json__()
    except:
        raise TypeError(f'Could not convert object to JSON: {obj}')


class DefaultJSONRendererPlugin:
    """Default JSON view renderer.

    Default JSON view renderer, available as 'default-json' in
    `turbogears.view.engines`. If no other plugin defines a 'json' engine,
    `view.engines['json']` will also refer to this renderer.

    Utilizes simplejson and a custom `default` function to automatically
    serialize

    * Decimal
    * date
    * datetime
    * UUID
    * any object with a `__json__` method

    If the incoming data is a `dict`, the renderer also removes TurboGears
    keys (any key starting with `tg_`) before serialization.

    """

    def __init__(self, extra_vars_fn=None, options=None):
        pass

    def render(self, info, format=None, fragment=False, template=None):
        if isinstance(info, dict):
            info = {
                k:v for k, v in info.items()
                if not k.startswith('tg_')
            }

        return dumps(info, default=default).encode('utf-8')
