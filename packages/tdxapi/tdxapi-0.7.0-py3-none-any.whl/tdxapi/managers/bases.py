from functools import wraps

import attr


@attr.s
class TdxManager(object):
    dispatcher = attr.ib(repr=False, eq=False)


def tdx_method(method, url):
    def wrapper(f):
        f.method = method
        f.url = url

        @wraps(f)
        def wrapped(*args, **kwargs):
            return f(*args, **kwargs)

        return wrapped

    return wrapper
