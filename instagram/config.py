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
    'cookie': 'ig_did=C6C263B9-D9B6-4B9F-ACCB-2188B8356022; '
              'mid=Xu7IOwALAAFTC8q5p0MNxmvt2QkR; '
              'csrftoken=R0JpvBSazrVzObTzd0BeMCsegxdTEE0B; '
              'ds_user_id=8883396194; '
              'sessionid=8883396194%3AGY5jIskM7rVGIn%3A5; '
              'shbid=4419; '
              'shbts=1592707145.1604345; '
              'rur=FTW; '
              'urlgen="{\"185.168.20.41\": 9009\054 \"193.176.211.35\": 206092\054 '
              '\"103.212.222.70\": 45382\054 \"193.176.211.53\": 206092}'
              ':1jmqKn:G_EtONRk2iCuvEThcn8LrBCrPUQ"',
}

proxies = {
    'http': 'http://127.0.0.1:10809',
    'https': 'https://127.0.0.1:10809'
}

query_hash_uri = 'https://www.instagram.com/static/bundles' \
                 '/metro/ProfilePageContainer.js/b5e793e9399f.js'

special_query_hash = 'eddbde960fed6bde675388aac39a3657'  # rogerfederer
