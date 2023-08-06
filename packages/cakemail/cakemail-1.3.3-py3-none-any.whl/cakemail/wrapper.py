from functools import wraps

from cakemail.response import Response


def wrapper(method):
    @wraps(method)
    def wrapped(*args, **kwargs):
        obj = method(*args, **kwargs)
        return Response(obj)

    return wrapped


class WrappedApi:
    def __init__(self, superclass, namemap: dict):
        if isinstance(namemap, dict):
            for short, name in namemap.items():
                setattr(self, short, wrapper(getattr(superclass, name)))
