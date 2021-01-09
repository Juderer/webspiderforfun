#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time       : 2021/01/09 22:11
@Author     : Julius Lee
@File       : utils.py
@DevTool    : PyCharm
@CopyFrom   : https://github.com/tianyuningmou/Coord_Transform
"""
import math


class CrdntSysUtil(object):
    """Coordinate System Util Class
    """
    def __init__(self):
        self.x_pi = 3.14159265358979324 * 3000.0 / 180.0
        self.pi = 3.1415926535897932384626  # 圆周率
        self.a = 6378245.0  # 地球长半轴长度
        self.ee = 0.00669342162296594323  # 地球的角离心率
        self.interval = 0.000001  # 矫正参数

    def gcj02_to_bd09(self, lng, lat):
        """
        火星坐标系(GCJ-02)转百度坐标系(BD-09)：谷歌、高德——>百度
        :param lng:火星坐标经度
        :param lat:火星坐标纬度
        :return:列表返回
        """
        z = math.sqrt(lng * lng + lat * lat) + 0.00002 * math.sin(lat * self.x_pi)
        theta = math.atan2(lat, lng) + 0.000003 * math.cos(lng * self.x_pi)
        bd_lng = z * math.cos(theta) + 0.0065
        bd_lat = z * math.sin(theta) + 0.006
        return [bd_lng, bd_lat]

    def bd09_to_gcj02(self, bd_lon, bd_lat):
        """
        百度坐标系(BD-09)转火星坐标系(GCJ-02)：百度——>谷歌、高德
        :param bd_lat:百度坐标纬度
        :param bd_lon:百度坐标经度
        :return:列表返回
        """
        x = bd_lon - 0.0065
        y = bd_lat - 0.006
        z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * self.x_pi)
        theta = math.atan2(y, x) - 0.000003 * math.cos(x * self.x_pi)
        gc_lng = z * math.cos(theta)
        gc_lat = z * math.sin(theta)
        return [gc_lng, gc_lat]

    def wgs84_to_gcj02(self, lng, lat):
        """
        WGS84转GCJ02(火星坐标系)
        :param lng:WGS84坐标系的经度
        :param lat:WGS84坐标系的纬度
        :return:列表返回
        """
        # 判断是否在国内
        if self.out_of_china(lng, lat):
            return lng, lat
        dlng = self._transformlng(lng - 105.0, lat - 35.0)
        dlat = self._transformlat(lng - 105.0, lat - 35.0)
        radlat = lat / 180.0 * self.pi
        magic = math.sin(radlat)
        magic = 1 - self.ee * magic * magic
        sqrtmagic = math.sqrt(magic)
        dlat = (dlat * 180.0) / ((self.a * (1 - self.ee)) / (magic * sqrtmagic) * self.pi)
        dlng = (dlng * 180.0) / (self.a / sqrtmagic * math.cos(radlat) * self.pi)
        gclng = lng + dlng
        gclat = lat + dlat
        return [gclng, gclat]

    def gcj02_to_wgs84(self, lng, lat):
        """
        GCJ02(火星坐标系)转GPS84
        :param lng:火星坐标系的经度
        :param lat:火星坐标系纬度
        :return:列表返回
        """
        # 判断是否在国内
        if self.out_of_china(lng, lat):
            return lng, lat
        dlng = self._transformlng(lng - 105.0, lat - 35.0)
        dlat = self._transformlat(lng - 105.0, lat - 35.0)
        radlat = lat / 180.0 * self.pi
        magic = math.sin(radlat)
        magic = 1 - self.ee * magic * magic
        sqrtmagic = math.sqrt(magic)
        dlat = (dlat * 180.0) / ((self.a * (1 - self.ee)) / (magic * sqrtmagic) * self.pi)
        dlng = (dlng * 180.0) / (self.a / sqrtmagic * math.cos(radlat) * self.pi)
        wgslng = lng + dlng
        wgslat = lat + dlat

        # 新加误差矫正部分
        corrent_list = self.wgs84_to_gcj02(wgslng, wgslat)
        clng = corrent_list[0] - lng
        clat = corrent_list[1] - lat
        dis = math.sqrt(clng * clng + clat * clat)

        while dis > self.interval:
            clng = clng / 2
            clat = clat / 2
            wgslng = wgslng - clng
            wgslat = wgslat - clat
            corrent_list = self.wgs84_to_gcj02(wgslng, wgslat)
            cclng = corrent_list[0] - lng
            cclat = corrent_list[1] - lat
            dis = math.sqrt(cclng * cclng + cclat * cclat)
            clng = clng if math.fabs(clng) > math.fabs(cclng) else cclng
            clat = clat if math.fabs(clat) > math.fabs(cclat) else cclat

        return [wgslng, wgslat]

    def bd09_to_wgs84(self, bd_lon, bd_lat):
        lon, lat = self.bd09_to_gcj02(bd_lon, bd_lat)
        return self.gcj02_to_wgs84(lon, lat)

    def wgs84_to_bd09(self, lon, lat):
        lon, lat = self.wgs84_to_gcj02(lon, lat)
        return self.gcj02_to_bd09(lon, lat)

    def _transformlat(self, lng, lat):
        ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
              0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
        ret += (20.0 * math.sin(6.0 * lng * self.pi) + 20.0 *
                math.sin(2.0 * lng * self.pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lat * self.pi) + 40.0 *
                math.sin(lat / 3.0 * self.pi)) * 2.0 / 3.0
        ret += (160.0 * math.sin(lat / 12.0 * self.pi) + 320 *
                math.sin(lat * self.pi / 30.0)) * 2.0 / 3.0
        return ret

    def _transformlng(self, lng, lat):
        ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
              0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
        ret += (20.0 * math.sin(6.0 * lng * self.pi) + 20.0 *
                math.sin(2.0 * lng * self.pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lng * self.pi) + 40.0 *
                math.sin(lng / 3.0 * self.pi)) * 2.0 / 3.0
        ret += (150.0 * math.sin(lng / 12.0 * self.pi) + 300.0 *
                math.sin(lng / 30.0 * self.pi)) * 2.0 / 3.0
        return ret

    def out_of_china(self, lng, lat):
        """
        判断是否在国内，不在国内不做偏移
        :param lng: 经度
        :param lat: 纬度
        :return:
        """
        return not (lng > 73.66 and lng < 135.05 and lat > 3.86 and lat < 53.55)


if __name__ == '__main__':
    lng = 116.4889647
    lat = 39.9854645
    gis_util = CrdntSysUtil()
    result1 = gis_util.gcj02_to_bd09(lng, lat)
    result2 = gis_util.bd09_to_gcj02(lng, lat)
    result3 = gis_util.wgs84_to_gcj02(lng, lat)
    result4 = gis_util.gcj02_to_wgs84(lng, lat)
    result5 = gis_util.bd09_to_wgs84(lng, lat)
    result6 = gis_util.wgs84_to_bd09(lng, lat)

    print(result1, result2, result3, result4, result5, result6)
