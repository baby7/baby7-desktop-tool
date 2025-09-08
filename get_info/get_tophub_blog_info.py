#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
    name:       获取信息
    by:         baby7
    blog:       https://www.baby7blog.com
    annotation: 获取信息
"""
import time
import random
import requests
from lxml import etree


def get_base_info():
    try:
        # 输出时间戳
        now_timestamp = int(time.time() * 1000)
        sina_global = str(int(random.random() * 10000000000000)) + "." + str(int(random.random() * 10000)) \
            + "." + str(now_timestamp - 14 - 1072340 - 6)
        apache = str(int(random.random() * 10000000000000)) + "." + str(int(random.random() * 10000)) \
            + "." + str(now_timestamp - 14)
        ulv = str(now_timestamp) + ":2:2:2:" \
            + str(int(random.random() * 10000000000000)) + "." + str(int(random.random() * 10000)) \
            + "." + str(now_timestamp - 14) \
            + ":" + str(now_timestamp - 14 - 1072340)
        cookie_result = 'SUB=_2AkMUqfltf8NxqwJRmPEVz2Pib4V_zwrEieKi9Qi2JRMxHRl-yT9kqk0ttRB6PynXgT5CUZzGwlh-mIyUQvhe-_yXXtj3; ' + \
                        'SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WFyRDSrne6a4e.bkQHJzd-.; ' + \
                        'SINAGLOBAL=' + sina_global + '; _s_tentry=-; ' + \
                        'Apache=' + apache + '; ' + \
                        'ULV=' + ulv
        # 请求头
        header = {
            'cookie': cookie_result,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.50',
        }
        res = requests.get(url="https://tophub.today", headers=header, timeout=3)
        return res
    except Exception as e:
        print("Error:{0}".format(e))
    return {"text": "403 Forbidden"}


# 处理成可以展示的html
def change_style(res, type_name, logger):
    try:
        if "403 Forbidden" in str(res.text):
            return "Login"
        result = '<table><thead><tr class="thead_tr"><th class="th-01">序号</th><th class="th-02">关键词</th><th class="th-03"></th></tr></thead><tbody>'
        html = etree.HTML(res.text)  # 转化成html文件
        if type_name == "baidu":
            search_list = html.xpath('//div[@id="node-2"]/div/div[2]/div[1]/a')
        elif type_name == "bilibili":
            search_list = html.xpath('//div[@id="node-19"]/div/div[2]/div[1]/a')
        elif type_name == "zhihu":
            search_list = html.xpath('//div[@id="node-6"]/div/div[2]/div[1]/a')
        elif type_name == "douyin":
            search_list = html.xpath('//div[@id="node-221"]/div/div[2]/div[1]/a')
        elif type_name == "tencent":
            search_list = html.xpath('//div[@id="node-35059"]/div/div[2]/div[1]/a')
        else:
            return
        for search_item in search_list:
            # 热搜排名
            search_item_index = str(search_item.xpath(".//div/span[1]/text()")[0])
            # 热搜标题
            search_item_title = str(search_item.xpath(".//div/span[2]/text()")[0])
            # 热搜地址
            search_item_url = str(search_item.xpath("./@href")[0])
            # 热搜火爆度
            search_item_count = str(search_item.xpath(".//div/span[3]/text()")[0])
            # 组合数据
            result = result + '<tr class=""><td class="td-01 ranktop ranktop2">' + search_item_index + '</td>'
            result = result + '<td class="td-02"><a href="' + search_item_url + '" target="_blank">' + search_item_title + '</a>'
            result = result + '<span> ' + search_item_count + '</span></td></tr>'
        result = result + '</tbody></table>'
        return result
    except Exception as e:
        print("Error:{0}".format(e))
        logger.info("获取热搜错误:{0}".format(e))
    return ""
