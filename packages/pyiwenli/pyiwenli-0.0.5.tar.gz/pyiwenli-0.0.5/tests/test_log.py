#!/usr/bin/env python
'''
Author: iwenli
License: Copyright © 2020 iwenli.org Inc. All rights reserved.
Github: https://github.com/iwenli
Date: 2020-11-26 12:05:27
LastEditors: iwenli
LastEditTime: 2020-11-27 13:08:53
Description: ...
'''
__author__ = 'iwenli'
from pyiwenli.handlers import LogHandler, debug, warn


def test_log():
    logging1 = LogHandler('logfileName')
    logging1.debug(u"调试日志")
    logging1.info(u"INFO日志")
    logging1.warning(u"警告日志")
    logging1.error(u"错误日志")
    logging1.critical(u"致命日志")
    logging2 = LogHandler('logfileName')
    logging2.error('api error')


def test_static_log():
    debug(u"静态DEBUG日志")
    warn(u"静态警告日志")