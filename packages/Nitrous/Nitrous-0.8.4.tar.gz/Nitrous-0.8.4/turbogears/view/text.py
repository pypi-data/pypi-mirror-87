class DefaultTextRendererPlugin:
    """Default Text view renderer.

    Default Text view renderer, available as 'default-text' in
    `turbogears.view.engines`. If no other plugin defines a 'text' engine,
    `view.engines['text']` will also refer to this renderer.

    Returns the string representation of `info` as UTF-8.

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

        if isinstance(info, bytes):
            return info
        else:
            return str(info).encode('utf-8')
