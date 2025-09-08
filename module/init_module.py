# 基础包
import os
import logging
from PySide2 import QtCore, QtGui
from PySide2.QtCore import *
from PySide2.QtWidgets import QGraphicsDropShadowEffect

# 工具
from util import resolution_util

# 模块
from module import click_connect, update_info

# 初始化日志
import util.logger as logger

def init_module(main_object):
    # 初始化日志
    config_path = str(os.getcwd()) + r"\log.log"
    main_object.info_logger = logger.Logger(config_path, logging.ERROR, logging.DEBUG)
    main_object.info_logger.info(main_object.app_name + "启动中...")
    # 隐藏部分
    # main_object.weibo_text_browser.hide()
    main_object.top_area.hide()
    main_object.scroll_area.hide()
    main_object.looking_area.hide()
    main_object.reading_area.hide()
    main_object.todo_area.hide()
    # main_object.weibo_text_browser.setGeometry(QtCore.QRect(20, 500 - 55, 361, 520 + 15))
    main_object.top_area.setGeometry(QtCore.QRect(12, 440, 381, 581))
    main_object.todo_area.setGeometry(QtCore.QRect(12, 440, 381, 581))
    main_object.scroll_area.setGeometry(QtCore.QRect(12, 440, 381, 581))
    main_object.looking_area.setGeometry(QtCore.QRect(18, 440, 364, 581))
    main_object.reading_area.setGeometry(QtCore.QRect(18, 440, 364, 581))
    # 开始线程
    main_object.start_thread_list()
    main_object.info_logger.info(main_object.app_name + "线程启动完成")
    # 更新日期部分
    main_object.update_date_and_time_model(True)
    # 更新天气部分
    main_object.weather_black_image = QtGui.QPixmap(":img/weather/black80.png")
    main_object.weather_blue_image = QtGui.QPixmap(":img/weather/blue80.png")
    # main_object.weather_blue_image = QtGui.QPixmap(":img/weather/lightBlue80.png")
    main_object.weather_list = [
        {"image": main_object.weather_image_label_1, "info": main_object.weather_info_label_1, 'temp': main_object.weather_temp_label_1},
        {"image": main_object.weather_image_label_2, "info": main_object.weather_info_label_2, 'temp': main_object.weather_temp_label_2},
        {"image": main_object.weather_image_label_3, "info": main_object.weather_info_label_3, 'temp': main_object.weather_temp_label_3},
        {"image": main_object.weather_image_label_4, "info": main_object.weather_info_label_4, 'temp': main_object.weather_temp_label_4},
        {"image": main_object.weather_image_label_5, "info": main_object.weather_info_label_5, 'temp': main_object.weather_temp_label_5}
    ]
    main_object.update_weather_info()
    # 更新倒计时部分
    main_object.update_count_down_list_by_api()
    # 绑定按钮
    click_connect.click_connect(main_object)
    # 退出动画
    resolution_util.out_animation(main_object)
    label_list = [
        main_object.label,
        main_object.label_2,
        main_object.label_5,
        main_object.push_button_schedule,
        # main_object.push_button_60s_news,
        # main_object.push_button_weibo_info
    ]
    for label in label_list:
        shadow1 = QGraphicsDropShadowEffect()
        shadow1.setOffset(0, 0)  # 偏移
        shadow1.setBlurRadius(5)  # 阴影半径
        shadow1.setColor(QtCore.Qt.white)  # 阴影颜色
        label.setGraphicsEffect(shadow1)
    # 设置浏览器不打开链接
    main_object.weibo_text_browser.setOpenLinks(False)
    main_object.weibo_text_browser.setOpenExternalLinks(False)
    main_object.weibo_text_browser.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    main_object.weibo_text_browser.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    main_object.info_logger.info(main_object.app_name + "启动完成")
    # 喝水初始化
    main_object.init_config()
    update_info.check_v(main_object)