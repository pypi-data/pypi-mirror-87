#!/usr/bin/env python
'''
Author: iwenli
License: Copyright © 2020 iwenli.org Inc. All rights reserved.
Github: https://github.com/iwenli
Date: 2020-11-26 16:56:44
LastEditors: iwenli
LastEditTime: 2020-11-26 17:04:28
Description: 正则提取数据
'''
__author__ = 'iwenli'

from pyiwenli.core.const import REConst
import re


def get_any(pattern, txt):
    """
    正则提取内容
    返回提取的列表
    """
    return re.findall(pattern, txt)


def get_emails(txt):
    """
    提取邮箱
    返回邮件列表
    """
    return get_any(REConst.Email, txt)


def get_ips(txt):
    """
    提取 IP
    """
    return get_any(REConst.Ip, txt)


def get_urls(txt):
    """
    提取 网址
    """
    return get_any(REConst.Url, txt)


def get_mobiles(txt):
    """
    提取 手机号
    """
    return get_any(REConst.Mobile, txt)