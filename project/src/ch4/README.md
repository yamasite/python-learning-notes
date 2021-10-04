# 在 Python 中使用线程

本文以循序渐进的方式介绍如何在 Python 中使用线程。

## 使用单线程执行循环

```python
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

```

## 使用多线程执行循环

### 使用 Thread 模块

> 避免使用 Thread 模块。

```python
#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import _thread
from time import sleep, ctime

loops = [4, 2]


def loop(nloop, nsec, lock):
    print('start loop', nloop, 'at: ', ctime())
    sleep(nsec)
    print('loop', nloop, 'done at:', ctime())
    lock.release()


def main():
    print('starting at:', ctime())
    locks = []
    nloops = range(len(loops))

    for i in nloops:
        lock = _thread.allocate_lock()
        lock.acquire()
        locks.append(lock)

    for i in nloops:
        _thread.start_new_thread(loop, (i, loops[i], locks[i]))

    for i in nloops:
        while locks[i].locked(): pass

    print('all DONE at:', ctime())


if __name__ == '__main__':
    main()

```

### 使用 Threading 模块

#### 创建一个 Thread 实例并调用 Thread 类的方法

```python
#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import threading
from time import sleep, ctime

loops = [4, 2]


def loop(nloop, nsec):
    print('start loop', nloop, 'at: ', ctime())
    sleep(nsec)
    print('loop', nloop, 'done at:', ctime())


def main():
    print('starting at:', ctime())
    threads = []
    nloops = range(len(loops))

    for i in nloops:
        t = threading.Thread(target=loop, args=(i, loops[i]))
        threads.append(t)

    for i in nloops:
        threads[i].start()

    for i in nloops:
        threads[i].join()

    print('all DONE at:', ctime())


if __name__ == '__main__':
    main()

```

#### 创建 Thread 实例并传入可调用对象

```python
#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import threading
from time import sleep, ctime

loops = [4, 2]


class ThreadFunc(object):

    def __init__(self, func, args, name=''):
        self.name = name
        self.func = func
        self.args = args

    def __call__(self):
        self.func(*self.args)


def loop(nloop, nsec):
    print('start loop', nloop, 'at:', ctime())
    sleep(nsec)
    print('loop', nloop, 'done at:', ctime())


def main():
    print('starting at:', ctime())
    threads = []
    nloops = range(len(loops))

    for i in nloops:
        t = threading.Thread(
            target=ThreadFunc(loop, (i, loops[i]), loop.__name__)
        )
        threads.append(t)

    for i in nloops:
        threads[i].start()

    for i in nloops:
        threads[i].join()

    print('all DONE at:', ctime())


if __name__ == '__main__':
    main()
```

#### 派生 Thread 的子类并创建子类实例

文件另存为 `myThread.py`。

```python
#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import threading
from time import sleep, ctime

loops = [4, 2]


class MyThread(threading.Thread):
    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args

    def run(self):
        self.func(*self.args)


def loop(nloop, nsec):
    print('start loop', nloop, 'at:', ctime())
    sleep(nsec)
    print('loop', nloop, 'done at:', ctime())


def main():
    print('starting at:', ctime())
    threads = []
    nloops = range(len(loops))

    for i in nloops:
        t = MyThread(loop, (i, loops[i]), loop.__name__)
        threads.append(t)

    for i in nloops:
        threads[i].start()

    for i in nloops:
        threads[i].join()

    print('all DONE at:', ctime())


if __name__ == '__main__':
    main()



```

## 单线程与多线程执行对比

```python
#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from myThread import MyThread
from time import ctime, sleep


def fib(x):
    sleep(0.005)
    if x < 2:
        return 1
    return fib(x - 2) + fib(x - 1)


def fac(x):
    sleep(0.1)
    if x < 2:
        return 1
    return x * fac(x - 1)


def sum(x):
    sleep(0.1)
    if x < 2:
        return 1
    return x + sum(x - 1)


funcs = [fib, fac, sum]
n = 12


def main():
    nfuncs = range(len(funcs))

    print('*** SINGLE THREAD')
    for i in nfuncs:
        print('starting', funcs[i].__name__, 'at:', ctime())
        print(funcs[i](n))
        print (funcs[i].__name__, 'finished at:', ctime())

    print('*** MULTIPLE THREADS')
    threads = []
    for i in nfuncs:
        t = MyThread(funcs[i], (n,), funcs[i].__name__)
        threads.append(t)

    for i in nfuncs:
        threads[i].start()

    for i in nfuncs:
        threads[i].join()
        print(threads[i].get_result())

    print('all DONE')


if __name__ == '__main__':
    main()


```

```shell
*** SINGLE THREAD
starting fib at: Mon Oct  4 22:48:36 2021
233
fib finished at: Mon Oct  4 22:48:39 2021
starting fac at: Mon Oct  4 22:48:39 2021
479001600
fac finished at: Mon Oct  4 22:48:40 2021
starting sum at: Mon Oct  4 22:48:40 2021
78
sum finished at: Mon Oct  4 22:48:41 2021
*** MULTIPLE THREADS
starting fib at: Mon Oct  4 22:48:41 2021
starting fac at: Mon Oct  4 22:48:41 2021
starting sum at: Mon Oct  4 22:48:41 2021
sum finished at: Mon Oct  4 22:48:43 2021
fac finished at: Mon Oct  4 22:48:43 2021
fib finished at: Mon Oct  4 22:48:44 2021
233
479001600
78
all DONE
```