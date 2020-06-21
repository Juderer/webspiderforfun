# -*- coding: utf-8 -*-
'''
@Time       : 2020/06/21 10:33
@Author     : Julius Lee
@File       : spider.py
@DevTool    : PyCharm
@Info       : Spider for Instagram
'''
import re
import requests
import json
from instagram.config import headers, proxies, query_hash_uri, special_query_hash


pic_video_cnt = 0

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


# TODO::整合获取html内容功能，使其更完善更可用
def get_html(url):
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
    ''''''
    global pic_video_cnt
    print('Begin to prase the first page: {url}'.format(url=url))
    html = get_html(url)
    pattern = re.compile('.*window._sharedData = (.*?);</script>', re.S)
    item = pattern.findall(html)
    # with open('./data/shared_data.json', 'w') as f:
    #     f.write(item[0])
    data = json.loads(item[0])

    graphql = data['entry_data']['ProfilePage'][0]['graphql']
    user_id = graphql['user']['id']
    count = graphql['user']['edge_owner_to_timeline_media']['count']
    page_info = graphql['user']['edge_owner_to_timeline_media']['page_info']
    has_next_page = page_info['has_next_page']
    after = page_info['end_cursor']
    edges = graphql['user']['edge_owner_to_timeline_media']['edges']

    for edge in edges:
        if edge['node']['is_video']:
            video_url = edge['node']['display_url']
            print('video: {}'.format(video_url))
            pic_video_cnt += 1
        else:
            pic_url = edge['node']['display_url']
            print('picture: {}'.format(pic_url))
            pic_video_cnt += 1

    return user_id, count, has_next_page, after


def get_query_hash(uri=query_hash_uri):
    '''
    获取query_hash
    :param uri: js文件URI
    :return: query_hash
    '''
    html = get_html(uri)
    pattern = re.compile(r'queryId:"(.*?)",', re.S)
    query_hashs = pattern.findall(html)
    print('query hash: {}'.format(query_hashs))
    return query_hashs[2]


def get_next_page(query_hash, user_id, has_next_page, after):
    ''''''
    global pic_video_cnt
    url = 'https://www.instagram.com/graphql/query/?'
    query_hash = special_query_hash
    while has_next_page:  # 判断是否有下一页
        #TODO::first为12时，会报错，未排查问题
        params = {
            'query_hash': query_hash,
            # 大括号是特殊转义字符，如果需要原始的大括号,用{{代替{
            'variables': '{{"id":"{}","first":50,"after":"{}"}}'.format(user_id, after),
        }

        # 另一种生成URI的方法
        # variables = {
        #     'id': user_id,
        #     'first': 50,
        #     'after': after,
        # }
        # next_url = 'https://www.instagram.com/graphql/query/?query_hash={}&variables={}' \
        #     .format(query_hash, json.dumps(variables))
        # print(next_url)
        # response = requests.get(next_url, headers=headers, proxies=proxies)

        try:
            response = requests.get(url, params=params, headers=headers, proxies=proxies)
        except Exception as e:
            raise e

        if response.status_code == 200:
            html = response.text
        else:
            raise Exception('请求网页源代码错误, 错误状态码：', response.status_code)

        content = json.loads(html)
        edges = content['data']['user']['edge_owner_to_timeline_media']['edges']
        page_info = content['data']['user']['edge_owner_to_timeline_media']['page_info']
        has_next_page = page_info['has_next_page']
        after = page_info['end_cursor']

        for edge in edges:
            if edge['node']['is_video']:
                video_url = edge['node']['video_url']
                print('video: {}'.format(video_url))
                pic_video_cnt += 1
            else:
                pic_url = edge['node']['display_url']
                print('picture: {}'.format(pic_url))
                pic_video_cnt += 1
    print(pic_video_cnt)

def run():
    url = get_blogger_homepage_url()
    # url = 'https://www.instagram.com/garbimuguruza/'
    user_id, count, has_next_page, after = parse_first_page(url)
    query_hash = get_query_hash()
    get_next_page(query_hash, user_id, has_next_page, after)

    return count

if __name__ == '__main__':
    if run() == pic_video_cnt:
        print('Data crawl completed！')
    else:
        # raise ValueError('爬取数据与实际数据不匹配')
        raise ValueError('The crawl data does not match the actual data')
