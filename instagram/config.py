#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time       : 2020/10/18 12;33
@Author     : Julius Lee
@File       : config.py
@DevTool    : PyCharm
@Info       : configuration file
"""
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/74.0.3729.131 Safari/537.36',
    'cookie': '',
}

proxies = {
    'http': 'http://127.0.0.1:10809',
    'https': 'https://127.0.0.1:10809'
}

query_hash_uri = 'https://www.instagram.com/static/bundles' \
                 '/metro/ProfilePageContainer.js/b5e793e9399f.js'

special_query_hash = 'eddbde960fed6bde675388aac39a3657'  # rogerfederer
