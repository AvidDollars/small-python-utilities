from typing import Callable
from datetime import datetime
import asyncio


def make_profile(func: Callable, dump_stats: bool = True):
    import cProfile
    import pstats

    def datetime_now():
        return datetime.now().strftime("%Y-%m-%dT%H-%M-%S")

    def generate_filename():
        return f"{datetime_now()}.prof"

    def is_async(func: Callable):
        return asyncio.iscoroutinefunction(func)

    with cProfile.Profile() as pr:
        if is_async(func):
            asyncio.run(func())
        else:
            func()

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)

    if dump_stats:
        """
        for visualizing statistics:
            cmd: pip install snakeviz
            cmd: snakeviz <filename>
        """
        filename = generate_filename()
        stats.dump_stats(filename)

    else:
        stats.print_stats()