import settings


def use_middleware(middlewares=None):
    def _use_middleware(func):
        def wrapper(*args, **kwargs):
            _middlewares = settings.MIDDLEWARES.get(str(middlewares)) or middlewares

            if _middlewares:
                _func = func

                for middleware in _middlewares:
                    _func = middleware(lambda: _func(*args, **kwargs), *args, **kwargs)
                return _func
            else:
                return func(*args, **kwargs)

        return wrapper

    return _use_middleware
