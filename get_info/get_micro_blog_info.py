#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
    name:       获取微博信息
    by:         baby7
    blog:       https://www.baby7blog.com
    annotation: 获取微博信息，例如热搜榜等
"""
import re
import time
import random
import requests
from lxml import etree
from urllib.parse import quote

import browser_cookie3

__all__ = ['judge_add']


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
        res = requests.get(url="https://s.weibo.com/top/summary?cate=realtimehot", headers=header, timeout=3)
        return res
    except Exception as e:
        print("Error:{0}".format(e))
    return {"text": "403 Forbidden"}


def get_hot_search_list(search_all, screen_word_list, screen_type_list, logger):
    """
    获取热搜榜（screen_word_list和screen_type_list为并集，不是交集）
    :param search_all: 查询所有的，优先级高于后面的筛选
    :param screen_word_list: 筛选关键词列表，为空表示不查询，进行筛序的话例如:['流浪地球', '刘德华']
    :param screen_type_list: 筛选类型列表，为空表示不查询，进行筛序的话例如:['new'(新),'hot'(热),'boil'(沸),'boom'(爆)]
    :return: 热搜榜
    """
    try:
        res = get_base_info()
        if "403 Forbidden" in str(res.text):
            return "Login"
        # print(res.text)
        html = etree.HTML(res.text)  # 转化成html文件
        hot_search_list = []
        if "pl_top_realtimehot" not in str(res.text):
            search_list = html.xpath("//section[@class='list']/ul/li")  # 提取数据
            for search_item in search_list:
                search_item_type = search_item.xpath(".//strong/@class")
                # 排除非热搜榜的信息
                if search_item_type is None or len(search_item_type) == 0 or search_item_type[0] != "hot":
                    continue
                # 热搜排名
                search_item_index = str(search_item.xpath(".//strong/text()")[0])
                # 热搜标题
                search_item_title = str(search_item.xpath(".//span/text()")[0])
                # 热搜地址(这里无法使用带参数的地址，如果使用win10通知会不展示)
                # search_item_url = "https://s.weibo.com" + \
                #                   str(search_item.xpath(".//a/@href")[0]).split("%23&t=")[0]
                search_item_url = "https://s.weibo.com/weibo?q=" + quote("#" + search_item_title + "#")
                # 热搜火爆度
                search_item_count_data = search_item.xpath(".//span/em/text()")
                search_item_count = str(search_item_count_data[0]).replace(" ", "").replace("电影", "").replace("综艺", "")\
                    .replace("剧集", "").replace("音乐", "") if \
                    search_item_count_data is not None and len(search_item_count_data) > 0 else None
                # 热搜图标，"icon icon_new"表示新，"icon icon_hot"表示热，"icon icon_boil"表示沸，"icon icon_boom"表示爆
                search_item_icon_data = search_item.xpath(".//i/@class")
                search_item_icon = str(search_item_icon_data[0]) if \
                    search_item_icon_data is not None and len(search_item_icon_data) > 0 else None
                # 组合数据
                search_item_data = {
                    "index": search_item_index,
                    "title": search_item_title,
                    "url": search_item_url,
                    "count": search_item_count,
                    "icon": search_item_icon,
                }
                if judge_add(search_all, screen_word_list, screen_type_list, search_item_data):
                    hot_search_list.append(search_item_data)
        else:
            search_list = html.xpath('//div[@id="pl_top_realtimehot"]/table/tbody/tr')  # 提取数据
            for search_item in search_list:
                search_item_type = search_item.xpath('.//td[@class="td-01 ranktop"]/text()')
                # 排除非热搜榜的信息
                if search_item_type is None or len(search_item_type) == 0 or search_item_type[0] == '•':
                    continue
                # 热搜排名
                search_item_index = str(search_item_type[0])
                # 热搜标题
                search_item_title = str(search_item.xpath('.//td[@class="td-02"]/a/text()')[0])
                # 热搜地址(这里无法使用带参数的地址，如果使用win10通知会不展示)
                # search_item_url = "https://s.weibo.com" + \
                #                   str(search_item.xpath('.//td[@class="td-02"]/a/@href')[0]).split("%23&t=")[0]
                search_item_url = "https://s.weibo.com/weibo?q=" + quote("#" + search_item_title + "#")
                # 热搜火爆度
                search_item_count_data = search_item.xpath('.//td[@class="td-02"]/span/text()')
                search_item_count = str(search_item_count_data[0]).replace(" ", "").replace("电影", "").replace("综艺", "")\
                    .replace("剧集", "").replace("音乐", "") if \
                    search_item_count_data is not None and len(search_item_count_data) > 0 else None
                # 热搜图标，"icon icon_new"表示新，"icon icon_hot"表示热，"icon icon_boil"表示沸，"icon icon_boom"表示爆
                search_item_icon_data = search_item.xpath('.//td[@class="td-03"]/i/@style')
                search_item_icon = str(search_item_icon_data[0]) if \
                    search_item_icon_data is not None and len(search_item_icon_data) > 0 else None
                if search_item_icon is not None:
                    if "#ff3852" in search_item_icon:
                        search_item_icon = "icon icon_new"
                    elif "#ff9406" in search_item_icon:
                        search_item_icon = "icon icon_hot"
                    elif "#f86400;" in search_item_icon:
                        search_item_icon = "icon icon_boil"
                    else:
                        search_item_icon = "icon icon_boom"
                # 组合数据
                search_item_data = {
                    "index": search_item_index,
                    "title": search_item_title,
                    "url": search_item_url,
                    "count": search_item_count,
                    "icon": search_item_icon,
                }
                if judge_add(search_all, screen_word_list, screen_type_list, search_item_data):
                    hot_search_list.append(search_item_data)
        return hot_search_list
    except Exception as e:
        print("Error:{0}".format(e))
        logger.info("获取微博热搜错误:{0}".format(e))
    return []


def judge_add(search_all,
              screen_word_list,
              screen_type_list,
              search_item_data):
    """
    根据筛选条件是否需要添加
    :param search_all: 查询所有的，优先级高于后面的筛选
    :param screen_word_list: 筛选关键词列表，为空表示不查询，进行筛序的话例如:['流浪地球', '刘德华']
    :param screen_type_list: 筛选类型列表，为空表示不查询，进行筛序的话例如:['new'(新),'hot'(热),'boil'(沸),'boom'(爆)]
    :param search_item_data: 单条热搜对象
    :return: True需要，False不需要
    """
    if search_all:
        return True
    else:
        # 进行关键词判断
        add_tag = False
        if screen_word_list is not None and len(screen_word_list) > 0:
            for screen_word in screen_word_list:
                if screen_word in search_item_data['title']:
                    add_tag = True
                    break
        # 进行类型判断
        if screen_type_list is not None and len(screen_type_list) > 0:
            if search_item_data['icon'] is not None:
                for screen_type in screen_type_list:
                    if screen_type in search_item_data['icon']:
                        add_tag = True
                        break
        if add_tag:
            return True
    return False


# 处理成可以展示的html
def change_css(html_content):
    # 热度标签样式
    html_content = html_content.replace("background-color:#bd0000;",
                        'background-color:#bd0000;display: inline-block;width: 16px;height: 16px;line-height: 16px;color: #fff;border-radius: 2px;text-align: center;font: 12px/1.3 Arial,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","WenQuanYi Micro Hei",sans-serif;')
    html_content = html_content.replace("background-color:#ff3852;",
                        'background-color:#ff3852;display: inline-block;width: 16px;height: 16px;line-height: 16px;color: #fff;border-radius: 2px;text-align: center;font: 12px/1.3 Arial,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","WenQuanYi Micro Hei",sans-serif;')
    html_content = html_content.replace("background-color:#ffab5a;",
                        'background-color:#ffab5a;display: inline-block;width: 16px;height: 16px;line-height: 16px;color: #fff;border-radius: 2px;text-align: center;font: 12px/1.3 Arial,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","WenQuanYi Micro Hei",sans-serif;')
    html_content = html_content.replace("background-color:#ff9406;",
                        'background-color:#ff9406;display: inline-block;width: 16px;height: 16px;line-height: 16px;color: #fff;border-radius: 2px;text-align: center;font: 12px/1.3 Arial,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","WenQuanYi Micro Hei",sans-serif;')
    html_content = html_content.replace("background-color:#f86400;",
                        'background-color:#f86400;display: inline-block;width: 16px;height: 16px;line-height: 16px;color: #fff;border-radius: 2px;text-align: center;font: 12px/1.3 Arial,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","WenQuanYi Micro Hei",sans-serif;')
    html_content = html_content.replace('>新<', '>&nbsp;新&nbsp;<')
    html_content = html_content.replace('>热<', '>&nbsp;热&nbsp;<')
    html_content = html_content.replace('>暖<', '>&nbsp;暖&nbsp;<')
    html_content = html_content.replace('>沸<', '>&nbsp;沸&nbsp;<')
    html_content = html_content.replace('>爆<', '>&nbsp;爆&nbsp;<')
    # 去掉顶部热搜
    matches = re.findall('<tr class="">\n.*<td class="td-01"><i class="icon-top">.*\n.*\n.*\n.*\n.*\n.*</tr>', html_content)
    for match in matches:
        html_content = html_content.replace(match, "")
    # 去掉广告
    matches = re.findall('<tr class="">\n.*<td class="td-01 ranktop".*\n.*\n.*\n.*\n.*\n.*\n.*</tr>', html_content)
    for match in matches:
        html_content = html_content.replace(match, "")
    # 去掉图片
    matches = re.findall('<img src.*">', html_content)
    for match in matches:
        html_content = html_content.replace(match, "")
    # 热搜文字样式
    for index in range(51):
        if index <= 3:
            html_content = html_content.replace('class="td-01 ranktop ranktop' + str(index) + '"',
                                                'class="td-01 ranktop ranktop' + str(index) + '" style="border-bottom:1px solid #f9f9f9;line-height:25px;color: #f26d5f;"')
        else:
            html_content = html_content.replace('class="td-01 ranktop ranktop' + str(index) + '"',
                                                'class="td-01 ranktop ranktop' + str(index) + '" style="border-bottom:1px solid #f9f9f9;line-height:25px;color: #ff8200;"')
    html_content = html_content.replace('class="td-02"',
                                        'class="td-02" style="border-bottom:1px solid #f9f9f9;line-height:25px;"')
    html_content = html_content.replace('class="td-03"',
                                        'class="td-03" style="border-bottom:1px solid #f9f9f9;line-height:25px;"')
    html_content = html_content.replace('target="_blank"',
                                        'target="_blank" style="text-decoration:none;color:#0078b6;"')
    html_content = html_content.replace('class="th-02"',
                                        'class="th-02" style="width:1000px;min-width:1000px;"')
    html_content = html_content.replace('</tbody>',
                                        '<tr style="line-height:1px;height: 1px;"><td></td><td><span style="color:white">'
                                        '————————————————————————————'
                                        '</span></td><td></td></tr></tbody>')
    return html_content


# screen_word_list = [
#     "流浪地球",
#     "刘德华",
#     "吴京",
#     "谢楠",
#     "郭帆"
# ]
# screen_type_list = [
#     # 'new',
#     # 'hot',
#     'boil',
#     'boom'
# ]
# hot_search_list = get_hot_search_list(False, screen_word_list, screen_type_list)
# for hot_search_data in hot_search_list:
#     icon_str = hot_search_data['icon']
#     if icon_str is None:
#         print(hot_search_data['index'] + ":  " + hot_search_data['title']
#               + "(" + hot_search_data['count'] + ")               " + hot_search_data['url'])
#     else:
#         type_str = "新" if icon_str == "icon icon_new" else \
#             "热" if icon_str == "icon icon_hot" else \
#             "沸" if icon_str == "icon icon_boil" else "爆"
#         print(hot_search_data['index'] + ":  " + hot_search_data['title']
#               + "(" + hot_search_data['count'] + ")"
#               + "     " + type_str + "           " + hot_search_data['url'])
