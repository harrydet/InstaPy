"""Helper module to handle time related stuff"""
import time
import threading
from functools import wraps
from random import gauss
from time import sleep as original_sleep

# Amount of variance to be introduced
# i.e. random time will be in the range: TIME +/- STDEV %
STDEV = 0.5
sleep_percentage = 1
logger = None

def randomize_time(mean):
    allowed_range = mean * STDEV
    stdev = allowed_range / 3  # 99.73% chance to be in the allowed range

    t = 0
    while abs(mean - t) > allowed_range:
        t = gauss(mean, stdev)

    return t

def set_sleep_percentage(percentage):
    global sleep_percentage
    sleep_percentage = percentage/100


def sleep(t, custom_percentage=None):
    if custom_percentage is None:
        custom_percentage = sleep_percentage
    time = randomize_time(t)/custom_percentage
    #print('\nSleeping for {} seconds\n'.format(time))
    original_sleep(time)

def sleep_actual(t):
  original_sleep(t)


def rate_limited(max_per_hour: int):
    """Rate-limits the decorated function locally, for one process."""
    lock = threading.Lock()
    min_interval = 3600 / max_per_hour

    def decorate(func):
        last_time_called = time.perf_counter()

        @wraps(func)
        def rate_limited_function(*args, **kwargs):
            lock.acquire()
            nonlocal last_time_called
            try:
                elapsed = time.perf_counter() - last_time_called
                left_to_wait = min_interval - elapsed
                if left_to_wait > 0:
                    time.sleep(left_to_wait)

                return func(*args, **kwargs)
            finally:
                last_time_called = time.perf_counter()
                lock.release()

        return rate_limited_function

    return decorate
