# -*- coding: utf-8 -*-
'''
@Time       : 2020/06/21 10:33
@Author     : Julius Lee
@File       : spider.py
@DevTool    : PyCharm
@Info       : Spider for Instagram
'''
import os
import re
import requests
import json
import threading
import hashlib
from instagram.config import headers, proxies, query_hash_uri, special_query_hash

pic_video_cnt = 0
pic_video_uris = {'picture': [], 'video': []}


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


def get_page_html(url, **kwargs):
    '''
    获取指定URL的内容
    :param url: URL for the new :class:`Request` object.
    :param kwargs: Optional arguments that ``request`` takes.
    :return: URL内容（str类型）
    '''
    try:
        response = requests.get(url, **kwargs)
        if response.status_code == 200:
            html = response.text
            return html
        else:
            raise Exception('请求网页源代码错误, 错误状态码：', response.status_code)
    except Exception as e:
        raise e


def parse_first_page(url):
    '''
    分析博主首页内容
    :param url:
    :return: 博主id，发布内容总数，是否有下一页，初始游标
    '''
    global pic_video_cnt, pic_video_uris
    print('Begin to prase the first page: {url}'.format(url=url))
    html = get_page_html(url, headers=headers, proxies=proxies)
    pattern = re.compile('.*window._sharedData = (.*?);</script>', re.S)
    item = pattern.findall(html)
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
            pic_video_uris['picture'].append(video_url)
        else:
            pic_url = edge['node']['display_url']
            print('picture: {}'.format(pic_url))
            pic_video_cnt += 1
            pic_video_uris['picture'].append(pic_url)

    return user_id, count, has_next_page, after


def get_query_hash(uri=query_hash_uri):
    '''
    获取query_hash
    :param uri: js文件URI
    :return: query_hash
    '''
    html = get_page_html(uri, headers=headers, proxies=proxies)
    pattern = re.compile(r'queryId:"(.*?)",', re.S)
    query_hashs = pattern.findall(html)
    print('query hash: {}'.format(query_hashs))
    return query_hashs[2]


def parse_next_page(query_hash, user_id, has_next_page, after):
    '''
    解析利用js动态生成的博主内容
    :param query_hash: 哈希码
    :param user_id: 博主ID
    :param has_next_page: 有无下一页
    :param after: 游标
    :return:
    '''
    global pic_video_cnt, pic_video_uris
    url = 'https://www.instagram.com/graphql/query/?'
    # TODO::自己解析的query_hash值有问题
    query_hash = special_query_hash
    while has_next_page:  # 判断是否有下一页
        # TODO::first为12时，会报错，未排查问题
        params = {
            'query_hash': query_hash,
            # 大括号是特殊转义字符，如果需要原始的大括号,用{{代替{
            'variables': '{{"id":"{}","first":30,"after":"{}"}}'.format(user_id, after),
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

        html = get_page_html(url, params=params, headers=headers, proxies=proxies)

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
                pic_video_uris['video'].append(video_url)
            else:
                pic_url = edge['node']['display_url']
                print('picture: {}'.format(pic_url))
                pic_video_cnt += 1
                pic_video_uris['picture'].append(pic_url)

    print(pic_video_cnt)


def mkdir_save_path(url):
    ''''''
    DATA_BASE_DIR = '{}/data/'.format(os.path.dirname(os.path.abspath(__file__)))
    if not os.path.exists(DATA_BASE_DIR):
        os.mkdir(DATA_BASE_DIR)
    user_name = re.split(r'/', url)[-2]
    if not os.path.exists(DATA_BASE_DIR + user_name):
        os.mkdir(DATA_BASE_DIR + user_name)
    save_pic_path = '{dir}{name}/pictures/'.format(dir=DATA_BASE_DIR, name=user_name)
    save_video_path = '{dir}{name}/videos/'.format(dir=DATA_BASE_DIR, name=user_name)
    for path in (save_pic_path, save_video_path):
        if not os.path.exists(path):
            os.mkdir(path)

    return save_pic_path, save_video_path


def md5(string):
    ''''''
    m = hashlib.md5()
    m.update(string.encode("utf8"))
    # print(m.hexdigest())
    return m.hexdigest()


def save_picture(save_path, uri):
    # pic_name = '{}.jpg'.format(md5(uri))
    # print(pic_name)
    print('Downloading picture: {}'.format(uri))
    response = requests.get(uri, headers=headers, proxies=proxies)
    pic_name = '{}.jpg'.format(hashlib.md5(response.content).hexdigest())
    if not os.path.exists(save_path + pic_name):
        with open(save_path + pic_name, 'wb') as f:
            f.write(response.content)


def save_video(save_path, uri):
    # video_name = '{}.jpg'.format(md5(uri))
    print('Downloading video: {}'.format(uri))
    response = requests.get(uri, headers=headers, proxies=proxies)
    video_name = '{}.mp4'.format(hashlib.md5(response.content).hexdigest())
    if not os.path.exists(save_path + video_name):
        with open(save_path + video_name, 'wb') as f:
            f.write(response.content)


def save_by_thread(save_pic_path, save_video_path, uris):
    t_objs = []
    pic_uris, video_uris = uris.values()
    for pic_uri in pic_uris:
        t = threading.Thread(target=save_picture, args=(save_pic_path, pic_uri))
        t.start()
        t_objs.append(t)
    for video_uri in video_uris:
        t = threading.Thread(target=save_video, args=(save_video_path, video_uri))
        t.start()
        t_objs.append(t)
    for t in t_objs:
        t.join()


def save_by_timeline(save_pic_path, save_video_path, uris):
    pic_uris, video_uris = uris.values()
    # for pic_uri in pic_uris:
    #     save_picture(save_pic_path, pic_uri)
    for video_uri in video_uris:
        save_video(save_video_path, video_uri)


def run():
    global pic_video_uris
    # url = get_blogger_homepage_url()
    url = 'https://www.instagram.com/garbimuguruza/'
    user_id, count, has_next_page, after = parse_first_page(url)
    query_hash = get_query_hash()
    parse_next_page(query_hash, user_id, has_next_page, after)

    save_pic_path, save_video_path = mkdir_save_path(url)
    save_by_timeline(save_pic_path, save_video_path, pic_video_uris)

    return count


if __name__ == '__main__':
    if run() == pic_video_cnt:
        print('Data crawl completed！')
    else:
        # raise ValueError('爬取数据与实际数据不匹配')
        raise ValueError('The crawl data does not match the actual data')
