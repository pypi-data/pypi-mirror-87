# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function

import time


def time_cost(func):
    def _time_cost(*args, **kwargs):
        start = time.time()
        ret = func(*args, **kwargs)
        print("==> time-cost: %4f (ms)     %s " % ((time.time() - start)*1000, func.__name__))
        return ret
    return _time_cost