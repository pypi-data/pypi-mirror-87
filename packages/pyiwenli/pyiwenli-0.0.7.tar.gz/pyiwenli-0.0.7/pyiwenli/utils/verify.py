#!/usr/bin/env python
'''
Author: iwenli
License: Copyright © 2020 iwenli.org Inc. All rights reserved.
Github: https://github.com/iwenli
Date: 2020-11-26 16:33:06
LastEditors: iwenli
LastEditTime: 2020-11-27 13:08:33
Description: 常用验证函数
'''
__author__ = 'iwenli'

from pyiwenli.core.const import REConst
import re


def is_any(pattern, txt):
    '''
    验证任意正则
    '''
    return re.match(pattern, txt) is not None


def is_mobile(txt):
    '''
    是否手机号
    '''
    return is_any(REConst.Mobile, txt)


def is_ip(txt):
    '''
    是否IP
    '''
    return is_any(REConst.Ip, txt)


def is_url(txt):
    '''
    是否 URL
    '''
    return is_any(REConst.Url, txt)


def is_email(txt):
    '''
    是否 email
    '''
    return is_any(REConst.Email, txt)