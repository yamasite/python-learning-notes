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