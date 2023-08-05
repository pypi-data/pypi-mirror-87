#!/usr/bin/env python
'''
Author: iwenli
License: Copyright © 2020 iwenli.org Inc. All rights reserved.
Github: https://github.com/iwenli
Date: 2020-11-26 11:37:46
LastEditors: iwenli
LastEditTime: 2020-11-26 16:28:29
Description: ...
'''
__author__ = 'iwenli'

from .logHandler import LogHandler, debug, info, warn, warning, error, fatal, critical
from .configHandler import ConfigHandler

# if __name__ == "__main__":
#     cfg1 = BookConfig()
#     cfg2 = BookConfig()
#     import operator
#     print(operator.eq(cfg1, cfg2))