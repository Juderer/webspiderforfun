# webspiderforfun
dev branch

## 1. instagram

爬取ins博主照片。

### TODO

* 视频只能下载第一帧，需要下载完整视频
* URL编码 
* hash算法的了解、尝试
* 参考github上其TA人写法，继续完善
* 考虑支持多个用户内容同时爬取
* **socks5**/**v2ray**/**http代理**等网络知识的进一步理解与探索

## 2. gaode API

调用高德API获取指定地点的经纬度。

* 可用API
    * [坐标获取](https://lbs.amap.com/console/show/picker)
    * [开发者API](https://lbs.amap.com/api)
        * [地理/逆地理编码](https://lbs.amap.com/api/webservice/guide/api/georegeo/)
            * 正地理编码：输入地址关键词，获得地址的经纬度
            * 逆地理编码：输入地址的经纬度，获得地址关键词
    
### TODO

* 模拟用户操作：selenium|chromedriver|phantomjs
