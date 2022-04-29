import functools
import operator
from typing import Callable, Generator, Iterable


class Stream:
    def __init__(self, data_source: Iterable):
        self._generator: Iterable | Generator = data_source

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._generator)

    # FILTER #
    def filter(self, predicate_fn: Callable) -> "Stream":
        def filter_data_gen(gen_obj: Generator, predicate_fn: Callable=predicate_fn) -> Generator:
            return (_ for _ in gen_obj if predicate_fn(_))

        self._generator = filter_data_gen(self._generator)
        return self

    # cases of filter function
    def less_than(self, number):
        self.filter(lambda inp: operator.lt(inp, number))
        return self

    def less_than_or_equal(self, number):
        self.filter(lambda inp: operator.le(inp, number))
        return self

    def greater_than(self, number):
        self.filter(lambda inp: operator.gt(inp, number))
        return self

    def greater_than_or_equal(self, number):
        self.filter(lambda inp: operator.ge(inp, number))
        return self

    # MAP #
    def map(self, map_fn: Callable) -> "Stream":
        def transform_data_gen(gen_obj: Generator, map_fn: Callable=map_fn) -> Generator:
            return (map_fn(_) for _ in gen_obj)

        self._generator = transform_data_gen(self._generator)
        return self

    # cases of map function
    def get_item_at_index(self, *indices: int) -> "Stream":
        self.map(operator.itemgetter(*indices))
        return self

    def get_length(self) -> "Stream":
        self.map(len)
        return self

    # REDUCE #
    def reduce(self, reduce_fn: Callable) -> "Stream":
        def reduce_data_gen(gen_obj: Generator, reduce_fn: Callable=reduce_fn) -> Generator:
            yield functools.reduce(reduce_fn, gen_obj)

        self._generator = reduce_data_gen(self._generator)
        return self

    # cases of reduce function
    def multiply(self) -> "Stream":
        self.reduce(operator.mul)
        return self

    def add(self) -> "Stream":
        self.reduce(operator.add)
        return self
