#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
    name:       获取天气信息
    by:         baby7
    blog:       https://www.baby7blog.com
    annotation: 来源地址: https://toy.lion1ou.tech/api/nowWeather 、 中国天气网
"""
import datetime

import requests
from lxml import html


weather_image_local_list = [
    {"name": "d0", "x": "0", "y": "0"},
    {"name": "d1", "x": "80", "y": "0"},
    {"name": "d2", "x": "160", "y": "0"},
    {"name": "d3", "x": "240", "y": "0"},
    {"name": "d4", "x": "320", "y": "0"},
    {"name": "d5", "x": "400", "y": "0"},
    {"name": "d6", "x": "480", "y": "0"},
    {"name": "d7", "x": "560", "y": "0"},
    {"name": "d8", "x": "640", "y": "0"},
    {"name": "d9", "x": "0", "y": "80"},
    {"name": "d00", "x": "0", "y": "0"},
    {"name": "d01", "x": "80", "y": "0"},
    {"name": "d02", "x": "160", "y": "0"},
    {"name": "d03", "x": "240", "y": "0"},
    {"name": "d04", "x": "320", "y": "0"},
    {"name": "d05", "x": "400", "y": "0"},
    {"name": "d06", "x": "480", "y": "0"},
    {"name": "d07", "x": "560", "y": "0"},
    {"name": "d08", "x": "640", "y": "0"},
    {"name": "d09", "x": "0", "y": "80"},
    {"name": "d10", "x": "80", "y": "80"},
    {"name": "d11", "x": "160", "y": "80"},
    {"name": "d12", "x": "240", "y": "80"},
    {"name": "d13", "x": "320", "y": "80"},
    {"name": "d14", "x": "400", "y": "80"},
    {"name": "d15", "x": "480", "y": "80"},
    {"name": "d16", "x": "560", "y": "80"},
    {"name": "d17", "x": "640", "y": "80"},
    {"name": "d18", "x": "0", "y": "160"},
    {"name": "d19", "x": "80", "y": "160"},
    {"name": "d20", "x": "160", "y": "160"},
    {"name": "d21", "x": "240", "y": "160"},
    {"name": "d22", "x": "320", "y": "160"},
    {"name": "d23", "x": "400", "y": "160"},
    {"name": "d24", "x": "480", "y": "160"},
    {"name": "d25", "x": "560", "y": "160"},
    {"name": "d26", "x": "640", "y": "160"},
    {"name": "d27", "x": "0", "y": "240"},
    {"name": "d28", "x": "80", "y": "240"},
    {"name": "d29", "x": "160", "y": "240"},
    {"name": "d30", "x": "240", "y": "240"},
    {"name": "d31", "x": "320", "y": "240"},
    {"name": "d32", "x": "400", "y": "240"},
    {"name": "d33", "x": "480", "y": "240"},
    {"name": "d53", "x": "560", "y": "240"},
    {"name": "d57", "x": "720", "y": "0"},
    {"name": "d32", "x": "720", "y": "80"},
    {"name": "d49", "x": "720", "y": "160"},
    {"name": "d58", "x": "720", "y": "240"},
    {"name": "d54", "x": "800", "y": "0"},
    {"name": "d55", "x": "800", "y": "80"},
    {"name": "d56", "x": "800", "y": "160"},
    {"name": "d301", "x": "880", "y": "0"},
    {"name": "d302", "x": "880", "y": "80"},
    {"name": "n0", "x": "0", "y": "320"},
    {"name": "n1", "x": "80", "y": "320"},
    {"name": "n2", "x": "160", "y": "320"},
    {"name": "n3", "x": "240", "y": "320"},
    {"name": "n4", "x": "320", "y": "320"},
    {"name": "n5", "x": "400", "y": "320"},
    {"name": "n6", "x": "480", "y": "320"},
    {"name": "n7", "x": "560", "y": "320"},
    {"name": "n8", "x": "640", "y": "320"},
    {"name": "n9", "x": "0", "y": "400"},
    {"name": "n00", "x": "0", "y": "320"},
    {"name": "n01", "x": "80", "y": "320"},
    {"name": "n02", "x": "160", "y": "320"},
    {"name": "n03", "x": "240", "y": "320"},
    {"name": "n04", "x": "320", "y": "320"},
    {"name": "n05", "x": "400", "y": "320"},
    {"name": "n06", "x": "480", "y": "320"},
    {"name": "n07", "x": "560", "y": "320"},
    {"name": "n08", "x": "640", "y": "320"},
    {"name": "n09", "x": "0", "y": "400"},
    {"name": "n10", "x": "80", "y": "400"},
    {"name": "n11", "x": "160", "y": "400"},
    {"name": "n12", "x": "240", "y": "400"},
    {"name": "n13", "x": "320", "y": "400"},
    {"name": "n14", "x": "400", "y": "400"},
    {"name": "n15", "x": "480", "y": "400"},
    {"name": "n16", "x": "560", "y": "400"},
    {"name": "n17", "x": "640", "y": "400"},
    {"name": "n18", "x": "0", "y": "480"},
    {"name": "n19", "x": "80", "y": "480"},
    {"name": "n20", "x": "160", "y": "480"},
    {"name": "n21", "x": "240", "y": "480"},
    {"name": "n22", "x": "320", "y": "480"},
    {"name": "n23", "x": "400", "y": "480"},
    {"name": "n24", "x": "480", "y": "480"},
    {"name": "n25", "x": "560", "y": "480"},
    {"name": "n26", "x": "640", "y": "480"},
    {"name": "n27", "x": "0", "y": "560"},
    {"name": "n28", "x": "80", "y": "560"},
    {"name": "n29", "x": "160", "y": "560"},
    {"name": "n30", "x": "240", "y": "560"},
    {"name": "n31", "x": "320", "y": "560"},
    {"name": "n32", "x": "400", "y": "560"},
    {"name": "n33", "x": "480", "y": "560"},
    {"name": "n53", "x": "560", "y": "560"},
    {"name": "n57", "x": "720", "y": "320"},
    {"name": "n32", "x": "720", "y": "400"},
    {"name": "n49", "x": "720", "y": "480"},
    {"name": "n58", "x": "720", "y": "560"},
    {"name": "n54", "x": "800", "y": "320"},
    {"name": "n55", "x": "800", "y": "400"},
    {"name": "n56", "x": "800", "y": "480"},
    {"name": "n301", "x": "880", "y": "320"}
]


def get_easy_weather_info(city_code=330106):
    """
    获取天气信息(toy.lion1ou.tech)，简易版本
    :param city_code: 城市代码，西湖表示330106
    :return:
    """
    data = {
        "city": str(city_code)
    }
    weather_info = requests.post(url="https://toy.lion1ou.tech/api/nowWeather", data=data).json()
    return weather_info['data']


def get_weather_info(city_code=101210101, days=6):
    """
    获取中国天气网信息
    :param city_code:101210101
    :return:
    """
    weather_list = []
    try:
        hour = datetime.datetime.today().hour
        url = 'http://www.weather.com.cn/weather/%s.shtml' % city_code
        content = requests.get(url, timeout=2).content
        sel = html.fromstring(content)
        top_list = sel.xpath('//ul[@class="t clearfix"]')[0]
        for i in range(1, days + 1):
            date = top_list.xpath('li[%d]/h1/text()' % i)[0]
            weather = top_list.xpath('li[%d]/p[@class="wea"]/text()' % i)[0]
            image = str(top_list.xpath('//*[@id="7d"]/ul/li[%d]/big[2]/@class' % i)[0]).split(" ")[1]
            if hour < 17:
                image = str(top_list.xpath('//*[@id="7d"]/ul/li[%d]/big[1]/@class' % i)[0]).split(" ")[1]
            temp = get_weather_tem(top_list, i)
            if "℃" not in str(temp):
                temp += "℃"
            weather_data = {
                "date": str(date).split("（")[0],
                "weather": weather,
                "temp": temp,
                "image": image
            }
            weather_list.append(weather_data)
    except Exception as e:
        print("Error:{0}".format(e))
    return weather_list


def get_weather_tem(top, index):
    """
    获取温度(供get_weather_info函数调用)
    """
    tem_low = top.xpath('li[%d]/p[@class="tem"]/i/text()' % index)[0]
    if len(top.xpath('li[%d]/p[@class="tem"]/span' % index)) != 0:
        tem_high = top.xpath('li[%d]/p[@class="tem"]/span/text()' % index)[0]
        return str(tem_low).replace("℃", "") + '~' + tem_high
    else:
        return tem_low


def get_weather_image(weather_data, base_image):
    """
    根据图片class提取图片
    :param weather_data: 天气图片json
    :param base_image: QPixmap格式的图片
    :return: 对应的天气图标
    """
    for weather_image_local in weather_image_local_list:
        if weather_image_local['name'] == weather_data['image']:
            return base_image.copy(int(weather_image_local['x']), int(weather_image_local['y']), 80, 80)
