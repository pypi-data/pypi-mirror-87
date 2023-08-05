#!/usr/bin/env python
'''
Author: iwenli
License: Copyright © 2020 iwenli.org Inc. All rights reserved.
Github: https://github.com/iwenli
Date: 2020-11-26 12:48:00
LastEditors: iwenli
LastEditTime: 2020-11-26 13:07:38
Description: ...
'''
__author__ = 'iwenli'
import time

# from utils.decoractors import timeit, logged
from pyiwenli.utils import timeit, logged


def test_timeit():
    @timeit('单元测试')
    def timeit_fun():
        time.sleep(2)

    timeit_fun()


def test_logged():
    @logged
    def logged_fun():
        time.sleep(2)

    logged_fun()