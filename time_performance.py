"""module for simple measuring time performance of functions"""

from time import perf_counter as _perf_counter
from functools import wraps as _wraps

def parameterized_timer(repeats=100_000):
    """a decorator factory used for timing purposes
    default value for repeats is set to 100_000

    eg:
        @parameterized_timer(repeats=1000)
        some_func():
            ...
    """
    def timer_decorator(fn):
        @_wraps(fn)
        def inner(*a, **kw):
            start = _perf_counter()
            for n in range(repeats-1):
                fn(*a, **kw)
            result = fn(*a, **kw)
            elapsed_time = _perf_counter() - start
            print(f"elapsed time of '{fn.__name__}': {round(elapsed_time, 3)}s (repeats={repeats})")
            return result
        return inner
    return timer_decorator

class timer:
    """
    timer aimed for comparing runtime of different functions
    usage:
        1) register a function you want to time with @register()
            - if decorated function takes arguments, they must be provided as parameters
              to @register()
            - if decorated function has default values, they can be overwritten by providing
              arguments to @register()
        2) after all functions are registered, perform timing with 'timer.run()'
            - number of iterations can be specified, the default is 'timer.run(repeats=1_000)'
    """

    registry = {}

    @classmethod
    def register(cls, *arg):
        def inner(fn):
            cls.registry[fn] = arg or fn.__defaults__ or ()
            return fn
        return inner

    @classmethod
    def run(cls, repeats=1_000):
        for fn, params in cls.registry.items():
            cls._timer(fn, repeats, *params)

    @staticmethod
    def _timer(fn, repeats, *arg):
        def inner(arg):
            start = _perf_counter()
            for n in range(repeats - 1):
                fn(*arg)
            result = fn(*arg)
            elapsed_time = _perf_counter() - start
            print(f"'{fn.__qualname__}':")
            print(f"\telapsed time: {elapsed_time:.3}s", end=", ")
            print("repeats: ", repeats, end=", ")
            print("result: ", result)
            print()
        return inner(arg)