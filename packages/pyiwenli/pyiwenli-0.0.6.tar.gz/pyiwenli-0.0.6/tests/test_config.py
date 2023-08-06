#!/usr/bin/env python
'''
Author: iwenli
License: Copyright © 2020 iwenli.org Inc. All rights reserved.
Github: https://github.com/iwenli
Date: 2020-11-26 16:27:06
LastEditors: iwenli
LastEditTime: 2020-11-27 13:08:43
Description: ...
'''
__author__ = 'iwenli'

from pyiwenli.handlers import ConfigHandler
from pyiwenli.core import LazyProperty


class TestConf(ConfigHandler):
    @LazyProperty
    def serverHost(self):
        return ConfigHandler.from_env("HOST", '127.0.0.1')


def test_conf():
    cfg1 = TestConf()
    cfg2 = TestConf()
    import operator
    print(operator.eq(cfg1, cfg2))
