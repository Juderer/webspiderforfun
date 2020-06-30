# -*- coding: utf-8 -*-
"""
@Time       : 2020/06/30 09:34
@Author     : Julius Lee
@File       : setup.py
@DevTool    : PyCharm
"""
from distutils.core import setup
from Cython.Build import cythonize

setup(
    name='instagram spider',
    version='1.0.0',
    ext_modules=cythonize('spider.py'),
    author='juliuslee'
)
