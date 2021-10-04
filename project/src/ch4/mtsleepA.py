#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import _thread
from time import sleep, ctime


def loop0():
    print('start loop 0 at:', ctime())
    sleep(4)
    print('loop 0 done at:', ctime())


def loop1():
    print('start loop 1 at:', ctime())
    sleep(2)
    print('loop 1 done at:', ctime())


def main():
    print('starting at:', ctime())
    # loop0()
    # loop1()
    _thread.start_new_thread(loop0, ())
    _thread.start_new_thread(loop1, ())
    sleep(6)
    print('all Done at:', ctime())


if __name__ == '__main__':
    main()

