from contextvars import ContextVar, Token


class _Wrapper:
    pass


v: ContextVar = ContextVar("everywhere.box")


class _Box(object):

    def __setattr__(self, key, value):
        try:
            var = v.get()
        except LookupError:
            var = _Wrapper()
            v.set(var)
        var.__setattr__(key, value)

    def __getattribute__(self, item):
        return getattr(v.get(), item)


class BoxContext:

    def __init__(self):
        self._token: Token

    def __enter__(self):
        self._token = v.set(_Wrapper())

    def __exit__(self, exc_type, exc_val, exc_tb):
        v.reset(self._token)


box = _Box()
