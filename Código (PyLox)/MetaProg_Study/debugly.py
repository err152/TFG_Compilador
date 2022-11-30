# debugly.py

from functools import wraps, partial

def debug(func=None, *, prefix=''):
    if func is None:
        # Wasn't passed
        return partial(debug, prefix=prefix)

    msg = prefix + func.__qualname__
    # func is function to be wrapped
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(msg)
        return func(*args, **kwargs)
    return wrapper

def debugmethods(cls):
    # cls is a class
    for key, val in vars(cls).items():
        if callable(val):
            setattr(cls, key, debug(val))

    return cls

