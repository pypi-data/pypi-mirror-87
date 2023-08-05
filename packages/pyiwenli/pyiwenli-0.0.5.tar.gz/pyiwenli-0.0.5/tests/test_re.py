#!/usr/bin/env python
'''
Author: iwenli
License: Copyright © 2020 iwenli.org Inc. All rights reserved.
Github: https://github.com/iwenli
Date: 2020-11-26 17:07:41
LastEditors: iwenli
LastEditTime: 2020-11-26 17:16:52
Description: ...
'''
__author__ = 'iwenli'

from pyiwenli.utils import get_ips, get_urls, get_emails, get_mobiles, is_ip


def test_verify_ip():
    txt = '1.1.1.1 asndfjubnsdf 192.168.1.128 18310807765 2344860@qq.com https://iwenli.org'
    ips = get_ips(txt)
    emails = get_emails(txt)
    urls = get_urls(txt)
    mobiles = get_mobiles(txt)
    assert len(ips) == 2
    assert len(emails) == 1
    assert len(urls) == 1
    assert len(mobiles) == 1
    
    for ip in ips:
        assert is_ip(ip) is True
