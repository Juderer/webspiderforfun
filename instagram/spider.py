# -*- coding: utf-8 -*-
'''
@Time       : 2020/06/21 10:33
@Author     : Julius Lee
@File       : spider.py
@DevTool    : PyCharm
@Info       : Spider for Istagram
'''
import re
import requests
import json
from instagram.config import headers, proxies


def get_ins_blogger_name():
    '''
    用户输入Instagram博主用户名
    :return: 博主用户名
    '''
    blogger_name = str(input("Please input the instagram blogger's name: "))
    return blogger_name.strip()


def get_blogger_homepage_url(default_name='garbimuguruza'):
    '''
    获取ins博主主页URL
    :param default_name: 默认访问garbimuguruza的ins主页
    :return: URL
    '''
    blogger_name = get_ins_blogger_name()
    if re.match(r'(\s|\n|\t)*', blogger_name).end() or blogger_name == '':
        blogger_name = default_name
    return 'https://www.instagram.com/{}/'.format(blogger_name)


def get_first_page_html(url):
    '''
    获取博主主页内容
    :param url: 博主主页
    :return: html内容
    '''
    try:
        response = requests.get(url, headers=headers, proxies=proxies)
        if response.status_code == 200:
            print('Visit successfully')
            html = response.text
            return html
        else:
            raise Exception('请求网页源代码错误, 错误状态码：', response.status_code)
    except Exception as e:
        raise e


def parse_first_page(url):
    print('Begin to prase the first page: {url}'.format(url=url))
    html = get_first_page_html(url)
    pattern = re.compile('.*window._sharedData = (.*?);</script>', re.S)
    item = re.findall(pattern, html)
    with open('./data/shared_data.json', 'w') as f:
        f.write(item[0])
    data = json.loads(item[0])

    graphql = data['entry_data']['ProfilePage'][0]['graphql']
    user_id = graphql['user']['id']
    page_info = graphql['user']['edge_owner_to_timeline_media']['page_info']
    next_page = page_info['has_next_page']
    after = page_info['end_cursor']
    edges = graphql['user']['edge_owner_to_timeline_media']['edges']
    display_urls = []
    for edge in edges:
        display_url = edge['node']['display_url']
        display_urls.append(display_url)
        print(display_url)

    return user_id, next_page, after


def run():
    # url = get_blogger_homepage_url()
    url = 'https://www.instagram.com/garbimuguruza/'
    user_id, next_page, after = parse_first_page(url)


if __name__ == '__main__':
    run()
