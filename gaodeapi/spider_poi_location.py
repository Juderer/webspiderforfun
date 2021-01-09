#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time       : 2021/01/05 22:11
@Author     : Julius Lee
@File       : spider_poi_location.py
@DevTool    : PyCharm
"""
import os
import sys
import requests
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gaodeapi.utils import CrdntSysUtil

conf_map = {}
with open('./self_conf.txt', 'r') as fd:
    for line in fd:
        key, value = line.strip().split(':')
        conf_map[key] = value
AMAP_KEY = conf_map['amap_key']
CITY = '北京'


class GeoLocation(object):
    def __init__(self, addr, lon_lat_str, city='北京'):
        """
        Location
        :param addr: 中文地址
        :param lon_lat_str: 默认GCJ02编码格式
        :param city: 默认北京
        """
        self.crdnt_sys_util = CrdntSysUtil()
        self.addr = addr
        if lon_lat_str is None or lon_lat_str is '':
            self.lon_gcj02, self.lat_gcj02 = None, None
            self.lon_wgs84, self.lat_wgs84 = None, None
        else:
            self.lon_gcj02, self.lat_gcj02 = (round(float(x), 6) for x in lon_lat_str.split(','))
            self.lon_wgs84, self.lat_wgs84 = (round(x, 6) for x in self.crdnt_sys_util.gcj02_to_wgs84(self.lon_gcj02,
                                                                                                      self.lat_gcj02))
        self.city = city

    def get_lon_lat_gcj02_str(self):
        return ','.join((str(x) for x in [self.lon_gcj02, self.lat_gcj02]))

    def get_lon_lat_wgs84_str(self):
        return ','.join(str(x) for x in [self.lon_wgs84, self.lat_wgs84])

    def __str__(self):
        geo_location_msgs = [self.addr, self.lon_gcj02, self.lat_gcj02]  # 默认以GCJ编码格式输出
        return ','.join((str(x) for x in geo_location_msgs))


def read_subway_station_name(filename):
    subway_line_no = None
    subway_station_name_map = {}
    with open(filename, 'r', encoding='utf-8') as fd:
        for line in fd:
            if 'line' in line and line.startswith('#'):
                subway_line_no = line.split(' ')[1].strip()
                subway_station_name_map[subway_line_no] = []
            elif line.startswith('('):
                pass  # 暂缓开通
            elif not 'line' in line and line.startswith('#'):
                pass  # 文件中注释
            else:
                subway_station_name_map[subway_line_no].append(line.strip())
    return subway_station_name_map


def get_location_by_subway_station_name(station_name, city='北京', output='JSON'):
    address = '{station_name}地铁站'.format(station_name=station_name)
    url = 'https://restapi.amap.com/v3/geocode/geo?address={}&city={}&output={}&key={}' \
        .format(address, city, output, AMAP_KEY)
    # TODO::出现莫名卡顿（很可能是网络问题）
    try:
        response = requests.get(url)
        if response.status_code == 200:
            result_map = json.loads(response.text)
        else:
            return None
    except Exception as e:
        print(e)
        return None
    formatted_addr = result_map['geocodes'][0]['formatted_address']
    lon_lat_str = result_map['geocodes'][0]['location']
    # TODO::判断查找或输出的地址是否是期望的
    if len(formatted_addr) < len(address) or not station_name in formatted_addr:
        return None
    return GeoLocation(formatted_addr, lon_lat_str)


def write2txt_file(subway_station_lct_list, txt_file_name='./subway_station_geo_msg.txt'):
    with open(txt_file_name, 'w', encoding='utf-8') as fd:
        for subway_station_lct in subway_station_lct_list:
            fd.write('{}\n'.format(str(subway_station_lct)))


def write2csv_file4qgis_software(subway_station_lct_list, csv_file_name='./subway_station_lon_lat.csv'):
    with open(csv_file_name, 'w', encoding='utf-8') as fd:
        for subway_station_lct in subway_station_lct_list:
            fd.write('{}\n'.format(subway_station_lct.get_lon_lat_gcj02_str()))


if __name__ == '__main__':
    subway_station_name_map = read_subway_station_name('./subway_station_name.txt')
    subway_station_lct_list = []
    for subway_line_no in subway_station_name_map:
        for station_name in subway_station_name_map[subway_line_no]:
            subway_station_lct = get_location_by_subway_station_name(station_name)
            if subway_station_lct:
                print(str(subway_station_lct))
                subway_station_lct_list.append(subway_station_lct)
            else:
                print('{} Not Found'.format(station_name))
                subway_station_lct_list.append(GeoLocation(station_name, ''))

    write2txt_file(subway_station_lct_list,
                   txt_file_name='subway_station_geo_msg_gcj02.txt')  # 高德使用GCJ02坐标系
    write2csv_file4qgis_software(subway_station_lct_list, csv_file_name='tst4qgis_gcj02.csv')
    print('finish')
