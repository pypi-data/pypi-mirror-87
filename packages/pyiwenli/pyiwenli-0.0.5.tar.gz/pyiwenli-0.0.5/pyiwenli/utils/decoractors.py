#!/usr/bin/env python
'''
Author: iwenli
License: Copyright © 2020 iwenli.org Inc. All rights reserved.
Github: https://github.com/iwenli
Date: 2020-11-26 11:45:29
LastEditors: iwenli
LastEditTime: 2020-11-27 13:08:23
Description: 常用装饰器
'''
__author__ = 'iwenli'

import functools
import time
from pyiwenli.handlers import LogHandler

__log = LogHandler("decoractors")


def omit_exception(func):
    '''
    异常忽略
    '''
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            __log.error(str(e))
            return None

    return wrap


def timeit(text):
    '''
    执行耗时统计
    '''
    def decorator(func):
        @functools.wraps(func)  # 防止函数now1.__name__ == wrapper
        def wrapper(*args, **kw):
            s = time.time()
            r = func(*args, **kw)
            __log.debug('[%s]-[%s()] 耗时: %s 秒' %
                        (text, func.__name__, time.time() - s))
            return r

        return wrapper

    return decorator


def logged(func):
    '''
    记录日志
    '''
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        __log.debug("执行方法：{}".format(func.__name__))
        return func(*args, **kwargs)

    return wrap

