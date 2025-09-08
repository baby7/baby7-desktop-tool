import datetime
import webbrowser

from PySide2.QtWidgets import QMessageBox

import util.send_win_message_util as send_message_util
from PySide2.QtCore import *

# 工具
from util import \
    time_util, \
    count_down_util

# 配置
from config import drinking_config

# 获取信息
from get_info import get_weather_info

def update_weather_info(main_object, city_code):
    try:
        weather_info_list = get_weather_info.get_weather_info(city_code)
        days = len(main_object.weather_list)
        for i in range(days):
            weather_message = weather_info_list[i]['weather']
            if "雨" in weather_message:
                weather_image = get_weather_info.get_weather_image(weather_info_list[i], main_object.weather_blue_image)
            else:
                weather_image = get_weather_info.get_weather_image(weather_info_list[i], main_object.weather_black_image)
            main_object.weather_list[i]['image'].setPixmap(weather_image)
            if i == 0:
                weather_info = "今天 " + weather_message
            else:
                weather_info = weather_info_list[i]['date'] + " " + weather_message
            if i == 0:
                main_object.weather_list[i]['info'].setText(weather_info)
            elif len(weather_info) >= 10 and i > 0:
                main_object.weather_list[i]['info'].setText(weather_info[0:int(len(weather_info) / 2) + 1] + "\n"
                                                     + weather_info[int(len(weather_info) / 2) + 1:])
            else:
                main_object.weather_list[i]['info'].setText(weather_info_list[i]['date'] + "\n"
                                                     + weather_message)
            main_object.weather_list[i]['temp'].setText(weather_info_list[i]['temp'])
        main_object.info_logger.info("天气更新完成")
    except Exception as e:
        print("Error:{}".format(e))


def update_date_and_time_model(main_object, update_time):
    """
    # 更新日期部分
    """
    today = datetime.datetime.today()
    main_object.info_logger.info(str(today.strftime("%Y年%m月%d日")))
    main_object.date_label.setText(time_util.get_chinese_date_str(today) + "    "
                            + time_util.get_week_str(today) + "\n"
                            + time_util.get_lunar_calendar_str(today) + "\n"
                            + time_util.get_constellation(today) + "    "
                            + time_util.get_week_by_year() + "    "
                            + time_util.get_holiday(today))
    if not update_time:
        return
    # 动态显示时间在label上
    main_object.timer = QTimer(main_object)
    # main_object.timer.setTimerType(Qt.PreciseTimer)
    main_object.timer.setInterval(100)
    main_object.timer.timeout.connect(main_object.showtime)
    main_object.timer.start()


def update_count_down_list_by_api(main_object):
    """
    基于接口的倒计时天数
    """
    try:
        holiday_list = count_down_util.holiday_data_list_timo()
        holiday_list_str = "\n".join(holiday_list[1:])
        main_object.daily_schedule_today.setText(holiday_list[0])
        main_object.daily_schedule_label.setText(holiday_list_str)
        main_object.info_logger.info("倒计时更新完成")
    except Exception as e:
        main_object.info_logger.error("{}".format(e))


def time_trigger_update(main_object, datetime_now_str):
    """
    定时刷新
    """
    try:
        print(datetime_now_str)
        datetime_now = datetime.datetime.strptime(datetime_now_str, "%Y-%m-%d %H:%M:%S")
        # 发送清单通知
        for open_todo_data in main_object.open_todo_data_list:
            if open_todo_data[4] and open_todo_data[5] == datetime_now_str:
                send_message_util.send_message(main_object.app_name, "待办清单任务通知", open_todo_data[1])
        for close_todo_data in main_object.close_todo_data_list:
            if close_todo_data[4] and close_todo_data[5] == datetime_now_str:
                send_message_util.send_message(main_object.app_name, "已办清单任务通知", close_todo_data[1])
        # 记录日志
        main_object.info_logger.info("定时刷新")
        # 更新日期部分
        main_object.update_date_and_time_model(False)
        # 更新天气部分
        if int(datetime_now.minute) % 10 == 0:
            main_object.update_weather_info()
        # 更新倒计时部分(如果零点需要重置)
        if int(datetime_now.hour) == 0 and int(datetime_now.minute) == 0:
            main_object.update_count_down_list_by_api()
        # 更新喝水(如果零点需要重置)
        if int(datetime_now.hour) == 0 and int(datetime_now.minute) == 0:
            main_object.schedule = 0
        # 记录喝水数据
        drinking_config.set_drinking_config({
            "date": str(datetime.date.today().strftime("%Y-%m-%d")),
            "count": main_object.schedule
        })
    except Exception as e:
        main_object.info_logger.error("{}".format(e))

def check_v(main_object):
    now = datetime.datetime.now()
    if now > datetime.datetime(2025, 9, 22):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("七仔的桌面工具")
        msg_box.setText("有新版本，优化了各项操作，增加了多种功能，强烈建议您前往下载！")
        # 设置背景色为白色，字体颜色为黑色
        msg_box.setStyleSheet(
            "QMessageBox { background-color: white; }"
            "QLabel { color: black; }"
        )
        # 创建自定义中文按钮
        download_button = msg_box.addButton("前往下载", QMessageBox.RejectRole)
        later_button = msg_box.addButton("稍后提醒", QMessageBox.AcceptRole)
        msg_box.setDefaultButton(download_button)
        result = msg_box.exec_()
        if msg_box.clickedButton() == download_button:
            # 打开浏览器
            dl_start = "https"
            dl_name = "agiletiles"
            dl_domain = ".".join([dl_name, "lanzoue", "com"])
            webbrowser.open(f"{dl_start}://{dl_domain}/s/{dl_name}")
            main_object.quit_before()
            exit()