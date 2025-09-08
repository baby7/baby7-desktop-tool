'''
**********************************热搜 · 开始***************************************
↓                                                                                 ↓
'''
top_open_style = """QPushButton {
    border-radius: 0px;
    background: rgb(255, 255, 255);
    border-bottom-left-radius: 4px;
    border-bottom-right-radius: 4px;
    border-style: solid;
    border: 2px solid #MAIN_COLOR;
    border-top-color: #ffffff;
    border-bottom-color: #MAIN_COLOR;
    border-left-color: #MAIN_COLOR;
    border-right-color: #MAIN_COLOR;
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
}
"""

top_close_style = """QPushButton {
    background: rgb(255, 255, 255);
    border-bottom-color: rgb(255, 255, 255);
    border-bottom-left-radius: 4px;
    border-bottom-right-radius: 4px;
}
QPushButton:hover {
    color: #TEXT_COLOR;
}
"""

top_line_style = """    color: #MAIN_COLOR;
    border-color: #MAIN_COLOR;
    background-color: #MAIN_COLOR;"""

top_weibo_text_color = "#FF8D16"
top_baidu_text_color = "#306eff"
top_bilibili_text_color = "#F58CAB"
top_zhihu_text_color = "#00a3ff"
top_douyin_text_color = "#ff1752"
top_tencent_text_color = "#fedc1c"
top_weibo_color = "#000"
top_baidu_color = "#000"
top_bilibili_color = "#000"
top_zhihu_color = "#000"
top_douyin_color = "#000"
top_tencent_color = "#000"


def get_top_style(tab, state):
    if tab == "weibo" and state:
        return top_open_style.replace("#MAIN_COLOR", top_weibo_color).replace("#TEXT_COLOR", top_weibo_text_color)
    if tab == "weibo" and not state:
        return top_close_style.replace("#MAIN_COLOR", top_weibo_color).replace("#TEXT_COLOR", top_weibo_text_color)
    if tab == "baidu" and state:
        return top_open_style.replace("#MAIN_COLOR", top_baidu_color).replace("#TEXT_COLOR", top_baidu_text_color)
    if tab == "baidu" and not state:
        return top_close_style.replace("#MAIN_COLOR", top_baidu_color).replace("#TEXT_COLOR", top_baidu_text_color)
    if tab == "bilibili" and state:
        return top_open_style.replace("#MAIN_COLOR", top_bilibili_color).replace("#TEXT_COLOR", top_bilibili_text_color)
    if tab == "bilibili" and not state:
        return top_close_style.replace("#MAIN_COLOR", top_bilibili_color).replace("#TEXT_COLOR", top_bilibili_text_color)
    if tab == "zhihu" and state:
        return top_open_style.replace("#MAIN_COLOR", top_zhihu_color).replace("#TEXT_COLOR", top_zhihu_text_color)
    if tab == "zhihu" and not state:
        return top_close_style.replace("#MAIN_COLOR", top_zhihu_color).replace("#TEXT_COLOR", top_zhihu_text_color)
    if tab == "douyin" and state:
        return top_open_style.replace("#MAIN_COLOR", top_douyin_color).replace("#TEXT_COLOR", top_douyin_text_color)
    if tab == "douyin" and not state:
        return top_close_style.replace("#MAIN_COLOR", top_douyin_color).replace("#TEXT_COLOR", top_douyin_text_color)
    if tab == "tencent" and state:
        return top_open_style.replace("#MAIN_COLOR", top_tencent_color).replace("#TEXT_COLOR", top_tencent_text_color)
    if tab == "tencent" and not state:
        return top_close_style.replace("#MAIN_COLOR", top_tencent_color).replace("#TEXT_COLOR", top_tencent_text_color)
    if tab == "todo" and state:
        return top_open_style.replace("#MAIN_COLOR", top_tencent_color).replace("#TEXT_COLOR", top_weibo_text_color)
    if tab == "todo" and not state:
        return top_close_style.replace("#MAIN_COLOR", top_tencent_color).replace("#TEXT_COLOR", top_weibo_text_color)
    if tab == "success" and state:
        return top_open_style.replace("#MAIN_COLOR", top_tencent_color).replace("#TEXT_COLOR", top_zhihu_text_color)
    if tab == "success" and not state:
        return top_close_style.replace("#MAIN_COLOR", top_tencent_color).replace("#TEXT_COLOR", top_zhihu_text_color)


def get_top_line_style(tab):
    if tab == "weibo":
        return top_line_style.replace("#MAIN_COLOR", top_weibo_color)
    if tab == "baidu":
        return top_line_style.replace("#MAIN_COLOR", top_baidu_color)
    if tab == "bilibili":
        return top_line_style.replace("#MAIN_COLOR", top_bilibili_color)
    if tab == "zhihu":
        return top_line_style.replace("#MAIN_COLOR", top_zhihu_color)
    if tab == "douyin":
        return top_line_style.replace("#MAIN_COLOR", top_douyin_color)
    if tab == "tencent":
        return top_line_style.replace("#MAIN_COLOR", top_tencent_color)
    if tab == "todo":
        return top_line_style.replace("#MAIN_COLOR", top_tencent_color)
    if tab == "success":
        return top_line_style.replace("#MAIN_COLOR", top_tencent_color)
'''
↑                                                                                ↑
**********************************热搜 · 结束***************************************
'''
'''
**********************************菜单 · 开始***************************************
↓                                                                                 ↓
'''
# menu_button_on = """    border-style: solid;
#     border-radius: 10px;
#     color: #FFFFFF;
#     border-color: #000000;
#     background-color: rgba(0, 0, 0, 0.3);
# """
# menu_button_off = """    border-style: solid;
#     border-radius: 10px;
#     border: 1px groove gray;
#     color: rgb(0, 0, 0);
#     border-color: rgba(0, 0, 0, 1);
#     background-color: rgba(255, 255, 255, 1);
# """
menu_button_on = """QPushButton {
    border-style: solid;
    border-radius: 10px;
    border: 0px groove gray;
    color: rgb(0, 0, 0);
    border-color: rgba(0, 0, 0, 1);
    background-color: rgba(255, 255, 255, 1);
}
"""
menu_button_off = """QPushButton {
    border-style: solid;
    border-radius: 10px;
    color: #FFFFFF;
    border-color: #000000;
    background-color: rgba(0, 0, 0, 0.3);
}
QPushButton:hover {
    background: rgba(255, 255, 255, 0.5);
    color: rgb(0, 0, 0);
}
"""


def get_menu_button_style(state):
    if state:
        return menu_button_on
    else:
        return menu_button_off
'''
↑                                                                                ↑
**********************************菜单 · 结束***************************************
'''