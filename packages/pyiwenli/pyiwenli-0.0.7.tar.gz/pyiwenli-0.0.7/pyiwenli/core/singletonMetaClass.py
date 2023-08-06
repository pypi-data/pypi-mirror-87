#!/usr/bin/env python
'''
Author: iwenli
License: Copyright © 2020 iwenli.org Inc. All rights reserved.
Github: https://github.com/iwenli
Date: 2020-11-25 16:05:23
LastEditors: iwenli
LastEditTime: 2020-11-25 16:16:59
Description: 单例
'''
__author__ = 'iwenli'


class SingletonMetaClass(type):
    """
    单例元类
    用法：
    class A (metaclass=SingletonMetaClass):
        pass
    """
    def __call__(cls, *args, **kwds):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__call__(*args, **kwds)
        return cls._instance
