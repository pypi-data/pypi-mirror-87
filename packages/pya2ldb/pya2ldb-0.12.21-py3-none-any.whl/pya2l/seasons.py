#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools

import numpy as np

#spring
summer = (np.arange(365) - 172 < 90) & (np.arange(365) - 172 > 0)
fall = (np.arange(365) - 262 < 90) & (np.arange(365) - 262 > 0)
winter = (np.arange(365) - 352 < 90) & (np.arange(365) - 352 > 0)

from datetime import date, datetime

Y = 2000 # dummy leap year to allow input X-02-29 (leap day)
seasons = [('winter', (date(Y,  1,  1),  date(Y,  3, 20))),
           ('spring', (date(Y,  3, 21),  date(Y,  6, 20))),
           ('summer', (date(Y,  6, 21),  date(Y,  9, 22))),
           ('autumn', (date(Y,  9, 23),  date(Y, 12, 20))),
           ('winter', (date(Y, 12, 21),  date(Y, 12, 31)))]

def get_season(now):
    if isinstance(now, datetime):
        now = now.date()
    now = now.replace(year=Y)
    return next(season for season, (start, end) in seasons
                if start <= now <= end)

print(get_season(date.today()))

def get_season(date):
    """
    convert date to month and day as integer (md), e.g. 4/21 = 421, 11/17 = 1117, etc.
    """
    m = date.month * 100
    d = date.day
    md = m + d

    if ((md >= 301) and (md <= 531)):
        s = 0  # spring
    elif ((md > 531) and (md < 901)):
        s = 1  # summer
    elif ((md >= 901) and (md <= 1130)):
        s = 2  # fall
#    elif ((md > 1130) and (md <= 0229)):
#        s = 3  # winter
    else:
        raise IndexError("Invalid date")

    return s

#season = get_season(dt.date())



def accepts(*types):
    def decorator(fn): 
        @functools.wraps(fn) 
        def inner(*args, **kwargs): 
            for (t, a) in zip(types, args): 
                assert isinstance(a, t) 
            return fn(*args, **kwargs) 
        return inner 
    return decorator

@accepts(int) 
def is_prime(n):
    pass

#is_prime(3.5)

import inspect

def enforce_types(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        sig = inspect.signature(f)
        for (name, param), value in zip(sig.parameters.items(), args):
            if param.annotation != inspect._empty:
                if not isinstance(value, param.annotation):
                    raise ValueError("Type check for '{}' failed. Excpected type {} got value {}".format(param.name, param.annotation, value))
        result = f(*args, **kwargs)
        if sig.return_annotation != inspect._empty:
            if not isinstance(result, sig.return_annotation):
                raise ValueError("Return check failed: needs to be of type {} got value {}".format(sig.return_annotation, result))
        return result
    return inner

@enforce_types
def foo_bar(a: int, b: float, c: int, d, **kws) -> float:
    return a * b + c

print(foo_bar(3, 5.3, 4, 7))

##
##
"""
primes: List[int] = []

captain: str  # Note: no initial value!

class Starship:
    stats: Dict[str, int] = {}
"""
