import time

from zuper_commons.timing import timeit_clock, timeit_wall
from . import logger


def test_time1():
    with timeit_clock("desc", logger):
        time.sleep(1)


def test_time2_wall():
    with timeit_wall("desc", logger):
        time.sleep(1)
