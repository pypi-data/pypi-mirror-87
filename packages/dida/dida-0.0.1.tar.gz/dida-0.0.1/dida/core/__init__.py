import functools

from .function import Function
from .scheduler import scheduler


def job(func=None, *, trigger=None):
    def decorator(fn):
        fn = functools.wraps(fn)(Function(fn))
        if trigger is not None:
            scheduler.add_job(fn, trigger)
        return fn

    if func is None:
        return decorator
    return decorator(func)
