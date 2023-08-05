import functools


def sofa_component(func):
    @functools.wraps(func)
    def wrapper_sofa_component(*args, **kwargs):
        defaults = dict(args[0]._defaults) if len(args)>0 else dict()
        infos = func(*args, **kwargs)
        name, params = infos if len(infos) == 2 else (infos, dict())
        params = {k: v for k, v in params.items() if v is not None}
        defaults.update(params)
        defaults.update(kwargs)
        return name, defaults

    return wrapper_sofa_component
