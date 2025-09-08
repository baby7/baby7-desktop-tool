#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
    name:       根据本机ip决定是否做域名映射
    by:         baby7
    blog:       https://www.baby7blog.com
    annotation: 解决内网无法访问本宽带公网ip的问题
"""
import socket


LAN_IP_1 = "192.168.4."                                    # 局域网固定ip(网线)
DNS_1 = "192.168.4.1 myself.baby7blog.com"                   # 域名解析(网线)
ANNOTATION_DNS_1 = "#192.168.4.1 myself.baby7blog.com"       # 注释掉的域名解析(网线)

LAN_IP_2 = "192.168.3."                                   # 局域网固定ip(wifi)
DNS_2 = "192.168.3.79 myself.baby7blog.com"                   # 域名解析(wifi)
ANNOTATION_DNS_2 = "#192.168.3.79 myself.baby7blog.com"       # 注释掉的域名解析(wifi)

HOST_PATH = r'C:\Windows\System32\drivers\etc\hosts'        # hosts文件地址


def change():
    """
    修改IP（自家用）
    """
    print("===================================开始host自动适应===================================")
    # 获取当前本机IP
    # ip = socket.gethostbyname(socket.gethostname())
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    print("当前ip为:" + str(ip))
    # 局域网需要做域名映射到内网ip
    file = open(HOST_PATH, "r+", encoding='utf-8')
    lines = file.readlines()
    line_192_168_4_1 = str(lines[0])
    line_192_168_3_79 = str(lines[1])
    edit_tag = False
    if LAN_IP_1 in str(ip):
        lines[0] = line_192_168_4_1.replace(ANNOTATION_DNS_1, DNS_1)
        if lines[0] != line_192_168_4_1:
            edit_tag = True
        if "#" not in line_192_168_3_79:
            lines[1] = line_192_168_3_79.replace(DNS_2, ANNOTATION_DNS_2)
            if lines[1] != line_192_168_3_79:
                edit_tag = True
        if not edit_tag:
            print("不需要修改host")
            print("===================================host自动适应完成===================================")
            return
        fo = open(HOST_PATH, "r+", encoding='utf-8')
        fo.writelines(lines)
    elif LAN_IP_2 in str(ip):
        if "#" not in line_192_168_4_1:
            lines[0] = line_192_168_4_1.replace(DNS_1, ANNOTATION_DNS_1)
            if lines[0] != line_192_168_4_1:
                edit_tag = True
        lines[1] = line_192_168_3_79.replace(ANNOTATION_DNS_2, DNS_2)
        if lines[1] != line_192_168_3_79:
            edit_tag = True
        if not edit_tag:
            print("不需要修改host")
            print("===================================host自动适应完成===================================")
            return
        fo = open(HOST_PATH, "r+", encoding='utf-8')
        fo.writelines(lines)
    else:
        if "#" not in line_192_168_4_1:
            lines[0] = line_192_168_4_1.replace(DNS_1, ANNOTATION_DNS_1)
            if lines[0] != line_192_168_4_1:
                print(lines[0])
                print(line_192_168_4_1)
                edit_tag = True
        if "#" not in line_192_168_3_79:
            lines[1] = line_192_168_3_79.replace(DNS_2, ANNOTATION_DNS_2)
            if lines[1] != line_192_168_3_79:
                print(lines[1])
                print(line_192_168_3_79)
                edit_tag = True
        if not edit_tag:
            print("不需要修改host")
            print("===================================host自动适应完成===================================")
            return
        fo = open(HOST_PATH, "r+", encoding='utf-8')
        fo.writelines(lines)
    print("===================================host自动适应完成===================================")
