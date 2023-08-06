import time
import functools


def timeit_decorator(func):
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        _t0 = time.time()
        _r = func(*args, **kwargs)
        _t1 = time.time()

        total_time = _t1 - _t0
        print(f"func [{func.__name__}], [{total_time}] seconds")
        return _r

    return wrap
