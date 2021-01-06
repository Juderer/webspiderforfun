#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time       : 2021/01/05 22:11
@Author     : Julius Lee
@File       : spider_location_lon_lat.py
@DevTool    : PyCharm
"""
import requests
import json

conf_map = {}
with open('./self_conf.txt', 'r') as fd:
    for line in fd:
        key, value = line.strip().split(':')
        conf_map[key] = value
AMAP_KEY = conf_map['amap_key']
CITY = '北京'


class GeoLocation(object):
    def __init__(self, addr, lon_lat_str):
        self.addr = addr
        self.lon, self.lat = (round(float(x), 6) for x in lon_lat_str.split(','))

    def __str__(self):
        geo_location_msgs = [self.addr, self.lon, self.lat]
        return ','.join((str(x) for x in geo_location_msgs))


def read_subway_station_name(filename):
    subway_line_no = None
    subway_station_name_map = {}
    with open(filename, 'r', encoding='utf-8') as fd:
        for line in fd:
            if line.startswith('#'):
                subway_line_no = line.split(' ')[1].strip()
                subway_station_name_map[subway_line_no] = []
            elif line.startswith('('):
                pass  # 暂缓开通
            else:
                subway_station_name_map[subway_line_no].append(line.strip())
    return subway_station_name_map


def get_location_by_subway_station_name(station_name, city='北京', output='JSON'):
    address = '{city}市{station_name}地铁站'.format(city=city, station_name=station_name)
    url = 'https://restapi.amap.com/v3/geocode/geo?address={}&city={}&output={}&key={}' \
        .format(address, city, output, AMAP_KEY)
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
    if len(formatted_addr) < len(address):
        return None
    return GeoLocation(formatted_addr, lon_lat_str)


subway_station_name_map = read_subway_station_name('./subway_station_name.txt')
for subway_line_no in subway_station_name_map:
    for station_name in subway_station_name_map[subway_line_no]:
        subway_geo_msg = get_location_by_subway_station_name(station_name)
        if subway_geo_msg:
            print(subway_geo_msg)
print('finish')
