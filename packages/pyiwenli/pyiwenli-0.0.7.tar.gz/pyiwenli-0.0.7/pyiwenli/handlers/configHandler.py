#!/usr/bin/env python
'''
Author: iwenli
License: Copyright © 2020 iwenli.org Inc. All rights reserved.
Github: https://github.com/iwenli
Date: 2020-11-26 13:59:11
LastEditors: iwenli
LastEditTime: 2020-11-27 13:07:57
Description: 配置
'''
__author__ = 'iwenli'

# from core import LazyProperty,SingletonMetaClass
from pyiwenli.core.lazyProperty import LazyProperty
from pyiwenli.core.singletonMetaClass import SingletonMetaClass
import os


class ConfigHandler(metaclass=SingletonMetaClass):
    """
    配置基类，单例
    延时对象

    用法：
    class TestConfig(ConfigHandler):
        @LazyProperty
        def serverHost(self):
            return from_env("HOST", '127.0.0.1')
    """
    pass

    def from_env(key, default=None):
        '''
        从环境变量获取配置
        '''
        return os.environ.get(key, default)
