#!/usr/bin/env python
'''
Author: iwenli
License: Copyright © 2020 iwenli.org Inc. All rights reserved.
Github: https://github.com/iwenli
Date: 2020-11-25 16:21:35
LastEditors: iwenli
LastEditTime: 2020-11-27 12:28:23
Description: 日志操作模块
'''
__author__ = 'iwenli'

import os, sys
import logging
import datetime
from logging.handlers import TimedRotatingFileHandler
from colorlog import ColoredFormatter

# 日志级别
CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0

_levelToName = {
    FATAL: 'FATAL',
    ERROR: 'ERROR',
    WARN: 'WARN',
    INFO: 'INFO',
    DEBUG: 'DEBUG',
}

# *文本记录路径
CURRENT_PATH = os.path.dirname(os.path.abspath(sys.argv[0]))
# ROOT_PATH = os.path.join(
#     CURRENT_PATH,
#     os.pardir,
# )

LOG_PATH = os.path.join(CURRENT_PATH, '_log',
                        datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
if not os.path.exists(LOG_PATH):
    try:
        os.makedirs(LOG_PATH)
    except FileExistsError:
        pass


class LogHandler(logging.Logger):
    """
    LogHandler
    """
    def __init__(self, name, level=DEBUG, stream=True, file=True):
        self.name = name
        self.level = level
        logging.Logger.__init__(self, self.name, level=level)
        if stream:
            self.__setStreamHandler__()
        if file:
            self.__setFileHandler__()

    def __setFileHandler__(self, level=None):
        """
        set file handler
        :param level:
        :return:
        """
        if level is None:
            level = self.level
        file_handler = LogHandler.__create_file_handler(self.name, level)
        self.file_handler = file_handler
        self.addHandler(file_handler)

    def __setStreamHandler__(self, level=None):
        """
        set stream handler
        :param level:
        :return:
        """
        stream_handler = logging.StreamHandler()
        formatter = ColoredFormatter(
            '%(asctime)s %(filename)s[line:%(lineno)d] %(log_color)s%(levelname)s %(message)s'
        )

        stream_handler.setFormatter(formatter)
        if level is None:
            stream_handler.setLevel(self.level)
        else:
            stream_handler.setLevel(level)
        self.addHandler(stream_handler)

    def __create_file_handler(file_name, level):
        full_name = os.path.join(LOG_PATH, '{name}.log'.format(name=file_name))
        # 设置日志回滚, 保存在log目录, 一天保存一个文件, 保留15天
        file_handler = TimedRotatingFileHandler(filename=full_name,
                                                when='D',
                                                interval=1,
                                                backupCount=15,
                                                encoding='utf-8')
        file_handler.suffix = '%Y%m%d.log'
        file_handler.setLevel(level)
        formatter = logging.Formatter(
            '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
        )

        file_handler.setFormatter(formatter)
        return file_handler


__loggers = {}


# 静态对象初始化  按错误类别记录的全局日志
def __generate_log(level):
    if (level not in __loggers):
        file_name = _levelToName[level].lower()
        log = LogHandler(file_name, level)
        __loggers.update({level: log})
    return __loggers[level]


def debug(msg, *args, **kwargs):
    '''
    静态记录日志到 debug 文件中
    '''
    __generate_log(DEBUG).debug(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    '''
    静态记录日志到 info 文件中
    '''
    __generate_log(INFO).info(msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    '''
    静态记录日志到 warn 文件中
    '''
    __generate_log(WARN).warning(msg, *args, **kwargs)


def warn(msg, *args, **kwargs):
    '''
    静态记录日志到 warn 文件中
    '''
    __generate_log(WARN).warning(msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    '''
    静态记录日志到 error 文件中
    '''
    __generate_log(ERROR).error(msg, *args, **kwargs)


def critical(msg, *args, **kwargs):
    '''
    静态记录日志到 fatal 文件中
    '''
    __generate_log(FATAL).critical(msg, *args, **kwargs)


def fatal(msg, *args, **kwargs):
    '''
    静态记录日志到 fatal 文件中
    '''
    __generate_log(FATAL).critical(msg, *args, **kwargs)
