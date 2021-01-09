# 使用高德开放API获取POI经纬度坐标

```text
|-- gaodeapi
    |-- __init__.py
    |-- utils.py
    |-- spider_poi_location.py
    |-- self_conf.txt  # 配置文件，像注册的高德开发者key等
    |-- readme.md
```

## utils.py

|类|说明|备注|
|:---:|:---:|:---:|
|CrdntSysUtil|此类用于百度坐标系（BD-09）、火星坐标系（GCJ02、国测局坐标系，高德等公司使用）、WGS84坐标系的相互转换|CopyFrom: https://github.com/tianyuningmou/Coord_Transform|

## spider_poi_location.py

获取地铁站POI的经纬度坐标（借助高德地理编码API）
