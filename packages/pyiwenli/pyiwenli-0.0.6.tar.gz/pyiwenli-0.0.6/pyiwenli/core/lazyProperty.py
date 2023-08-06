#!/usr/bin/env python
'''
Author: iwenli
License: Copyright © 2020 iwenli.org Inc. All rights reserved.
Github: https://github.com/iwenli
Date: 2020-11-25 15:54:29
LastEditors: iwenli
LastEditTime: 2020-11-25 15:57:42
Description: ...
'''
__author__ = 'iwenli'


class LazyProperty(object):
    """
    延迟属性
    """
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)
            return value
