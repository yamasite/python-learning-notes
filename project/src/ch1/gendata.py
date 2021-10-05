#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from random import randrange, choice
from string import ascii_lowercase as lc
from sys import maxsize
from time import ctime

tlds = ('com', 'edu', 'net', 'org', 'gov')

for i in range(randrange(5, 11)):
    dtint = randrange(start=0, stop=maxsize)
    print(dtint)
    # https://docs.python.org/3/library/datetime.html
    # fromtimestamp() may raise OverflowError, if the timestamp is out of the range of values supported by the platform
    # C localtime() or gmtime() functions, and OSError on localtime() or gmtime() failure.
    #
    # [...]
    #
    # Naive datetime instances are assumed to represent local time and this method relies on the platform C mktime()
    # function to perform the conversion. Since datetime supports wider range of values than mktime() on many platforms,
    # this method may raise OverflowError for times far in the past or far in the future.
    #
    # https://docs.microsoft.com/en-us/cpp/c-runtime-library/reference/localtime-localtime32-localtime64?redirectedfrom=MSDN&view=msvc-160
    # _localtime64, which uses the
    # __time64_t structure, allows dates to be expressed up through 23:59:59, December 31, 3000, coordinated universal time (UTC),
    # whereas _localtime32 represents dates through 23:59:59 January 18, 2038, UTC.
    # localtime is an inline function which evaluates to _localtime64, and time_t is equivalent to __time64_t.
    # If you need to force the compiler to interpret time_t as the old 32-bit time_t, you can define _USE_32BIT_TIME_T.
    # Doing this will cause localtime to evaluate to _localtime32. This is not recommended because
    # your application may fail after January 18, 2038, and it is not allowed on 64-bit platforms.

    dtstr = ctime(dtint/1000000000)
    llen = randrange(4, 8)
    login = ''.join(choice(lc) for j in range(llen))
    dlen = randrange(llen, 13)
    dom = ''.join(choice(lc) for j in range(dlen))
    print('%s::%s@%s.%s::%d-%d-%d' % (dtstr, login, dom, choice(tlds), dtint, llen, dlen))