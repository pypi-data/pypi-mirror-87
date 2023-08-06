#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : pipe_utils
# @Time         : 2020/11/12 11:35 上午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

import functools
from meutils.common import *


class Pipe(object):
    """I am very like a linux pipe"""

    def __init__(self, function):
        self.function = function
        functools.update_wrapper(self, function)

    def __ror__(self, other):
        return self.function(other)

    def __call__(self, *args, **kwargs):
        return Pipe(lambda x: self.function(x, *args, **kwargs))


########### 常用管道函数
# 进度条
xtqdm = Pipe(lambda iterable, desc=None: tqdm(iterable, desc))

# base types
xtuple, xlist, xset = Pipe(tuple), Pipe(list), Pipe(set)

# 高阶函数
xmap = (lambda iterable, func: map(func, iterable))
xreduce = Pipe(lambda iterable, func: reduce(func, iterable))
xfilter = Pipe(lambda iterable, func: filter(func, iterable))


# multiple
@Pipe
def xThreadPoolExecutor(iterable, func, max_workers=5):
    """
    with ThreadPoolExecutor(max_workers) as pool:
        pool.map(func, iterable)
    """
    with ThreadPoolExecutor(max_workers) as pool:
        return pool.map(func, iterable)


@Pipe
def xProcessPoolExecutor(iterable, func, max_workers=5):
    """
    with ProcessPoolExecutor(max_workers) as pool:
        pool.map(func, iterable)
    """
    with ProcessPoolExecutor(max_workers) as pool:
        return pool.map(func, iterable)


if __name__ == '__main__':
    @Pipe
    def xfunc1(x):
        _ = x.split()
        print(_)
        return _


    @Pipe
    def xfunc2(x):
        _ = '>>'.join(x)
        print(_)
        return _


    def wrapper(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            logger.patch(lambda r: r.update(name='__file__', function=func.__name__)).info("Wrapped!")
            return func(*args, **kwargs)

        return wrapped


    log = 'I am very like a linux pipe' | xfunc1 | xfunc2
    logger.info(log)

    logger = logger.patch(lambda r: r.update(name=__file__, function=''))  # main:module
    logger.info(log)

    logger = logger.patch(wrapper(lambda x: ''))
    logger.info(log)
