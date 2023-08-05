#!/usr/bin/env python
'''
Author: iwenli
License: Copyright © 2020 iwenli.org Inc. All rights reserved.
Github: https://github.com/iwenli
Date: 2020-11-26 17:24:43
LastEditors: iwenli
LastEditTime: 2020-11-27 13:19:09
Description: upload pip
'''
__author__ = 'iwenli'

from setuptools import setup, find_packages

setup(name="pyiwenli",
      version="0.0.5",
      keywords=("pip", "iwenli"),
      description="自用工具封装",
      long_description="",
      license="MIT Licence",
      url="https://github.com/iwenli/pyiwenli",
      author="iwenli",
      author_email="admin@iwenli.org",
      packages=find_packages(),
      include_package_data=True,
      platforms="any",
      install_requires=["colorlog==4.6.2"])
