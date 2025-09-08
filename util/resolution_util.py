#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
    name:       动画和分辨率工具
    by:         baby7
    blog:       https://www.baby7blog.com
    annotation: 分辨率参数初始化和动画执行
"""
from win32api import GetMonitorInfo, MonitorFromPoint
from PySide2.QtCore import QSequentialAnimationGroup, QPropertyAnimation, QRect, QEasingCurve
from PySide2.QtWidgets import QApplication


def init_resolution(main_window):
    """
    初始化分辨率参数
    :param main_window: 主窗口
    """
    desktop = QApplication.desktop().screenGeometry(0)  # 多显示屏，显示主屏
    main_window.desktop_width = desktop.width()
    main_window.desktop_height = desktop.height()
    # 屏幕信息
    monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
    monitor = monitor_info.get('Monitor')  # 屏幕分辨率
    work = monitor_info.get('Work')  # 工作区间
    # 缩放比例
    scaling = monitor[2] / main_window.desktop_width
    # 任务栏高度
    main_window.taskbar_height = int(int(monitor[3] - work[3]) / scaling)


def in_animation(main_window):
    """
    进入动画
    :param main_window: 主窗口
    :return:
    """
    # 从下到上
    # start_animation(
    #     main_window,
    #     main_window.desktop_width - main_window.width(),
    #     main_window.desktop_height,
    #     main_window.desktop_width - main_window.width(),
    #     main_window.desktop_height - main_window.height() - main_window.taskbar_height,
    # )
    # 从右到左
    main_window.show_form = True
    start_animation(
        main_window,
        main_window.desktop_width,
        0,
        main_window.desktop_width - main_window.width(),
        0,
    )


def out_animation(main_window):
    """
    退出动画
    :param main_window: 主窗口
    :return:
    """
    # 从上到下
    # start_animation(
    #     main_window,
    #     main_window.desktop_width - main_window.width(),
    #     main_window.desktop_height - main_window.height() - main_window.taskbar_height,
    #     main_window.desktop_width - main_window.width(),
    #     main_window.desktop_height,
    # )
    # 从左到右
    main_window.show_form = False
    start_animation(
        main_window,
        main_window.desktop_width - main_window.width(),
        0,
        main_window.desktop_width,
        0,
    )


def start_animation(main_window, start_x, start_y, end_x, end_y):
    """
    动画执行
    :param main_window: 主窗口
    :param start_x: 初始点x
    :param start_y: 初始点y
    :param end_x: 结束点x
    :param end_y: 结束点y
    :return:
    """
    main_window.group = QSequentialAnimationGroup()
    animation = QPropertyAnimation(main_window, b'geometry')
    main_window.group.addAnimation(animation)
    animation.setDuration(200)  # 持续时间
    animation.setStartValue(QRect(start_x, start_y, main_window.width(), main_window.height()))
    animation.setEndValue(QRect(end_x, end_y, main_window.width(), main_window.height()))
    # animation.setEasingCurve(QEasingCurve.OutBack)     # 动画特效
    animation.setEasingCurve(QEasingCurve.Linear)     # 动画特效
    main_window.group.start()
