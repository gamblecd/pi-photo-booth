import time
import math
def _count_helper(seconds, init_val, count_fn):
    start = int(time.time())
    now = int(time.time())
    val = init_val
    count = 0
    yield val
    while not count == seconds:
        if not (now - start) == count:
            val = count_fn(now, start)
            count += abs(val)
        yield val
        now = int(time.time())

def count_up(seconds):
    ''' Counts up from 0 to the number provided, increments once a second'''
    return _count_helper(seconds, 0, lambda x, y: (x-y))

def count_down(seconds):
    ''' Counts down from the number provided to 0, decrements once a second'''
    return _count_helper(seconds, seconds, lambda x, y: seconds - (x-y))
