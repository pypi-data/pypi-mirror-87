#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: lijin
# Mail: lijin@dingtalk.com
# Created Time:  2019-09-05
#############################################


from setuptools import setup, find_packages		# 没有这个库的可以通过pip install setuptools导入

setup(
    name = "pyormx",
    version = "0.2.1",
    keywords = ("pip", "pathtool","timetool", "magetool", "mage"),							
    description = "python简易ORM框架",
    long_description = "python简易ORM框架",
    license = "MIT Licence",

    url = "https://github.com/xingluoxingkong/pyormx",
    author = "xlxk",
    author_email = "xlxk@xlxk.top",

    packages = find_packages(),	
    include_package_data = True,
    platforms = "any",
    install_requires = []
)