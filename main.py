# 基础包
import sys
import uuid
import requests
import datetime
from lxml import etree
from functools import partial
# 资源包
import compiled_resources

# 界面
from qframelesswindow import AcrylicWindow
from baby7_desktop_tool_form import Ui_Form

# PySide2
from PySide2 import QtCore, QtGui
from PySide2.QtCore import *
from PySide2.QtWidgets import QApplication, QListWidgetItem, QMessageBox
from PySide2 import QtWidgets
from PySide2.QtCore import Qt

from my_component.MyQLabel import MyQLabel
from my_component.MyListWidget import MyQWidgetItem

# 工具
from util import \
    thread_util, \
    resolution_util, \
    browser_util, \
    show_image_util, \
    style_util, \
    version_util

# 界面
from setting import SettingWindow
from record import RecordWindow
from city import CityWindow
from new_todo import NewTodoWindow

# 配置
from config import drinking_config
import config.drinking_setting as drinking_setting
import config.city_setting as city_setting
import config.todo_list_config as todo_list_config

# 线程
from thread_list import time_thread, keyboard_thread

# 模块
from module import (icon_tool,
                    drink_paint,
                    update_info as update_info_module,
                    init_module)

# 获取信息
from get_info import get_micro_blog_info, get_tophub_blog_info


"""
生成exe的命令：
pyinstaller -F -w -i img/icon/icon.ico -n 七仔的桌面工具V2.5.0 main.py
pyinstaller -F -i img/icon/icon.ico -n 七仔的桌面工具V2.5.0 main.py
或使用nuitka
nuitka --mingw64 --onefile --standalone --windows-console-mode=disable --enable-plugin=pyside2 --include-package=win32com --include-package=pywintypes --windows-icon-from-ico=img/icon/icon.ico --output-dir=out --windows-uac-admin --lto=yes --jobs=14 --show-progress --show-memory main.py
"""


class MyForm(AcrylicWindow, Ui_Form):

    app_name = "七仔的桌面工具V2.5.0"              # 应用标题
    tray_icon = None                            # 图标
    timer = None                                # 时间
    web_view = None                             # 浏览器

    # 线程列表
    time_thread_object = None                   # 时间线程
    keyboard_thread_object = None               # 键盘监听线程
    schedule_thread_object = None               # 倒计时线程
    time_thread = None

    # 分辨率和动画信息
    taskbar_height = 0                          # 任务栏高度
    desktop_width = 0                           # 桌面宽度
    desktop_height = 0                          # 桌面高度
    group = None                                # 执行动画的对象
    show_form = False                           # 是否显示（隐藏是移动到窗口外）
    dialog_fault = None

    # 卡片
    image_card_data = None                      # 图片卡片数据
    cache_label = None                          # 卡片缓存
    see_card = "weibo"                          # 下方卡片中当前查看的是哪个卡片

    # 喝水
    text_color = "#000"                         # 文字颜色
    line_color = 0                              # 线条颜色
    pen = None                                  # 画笔
    background_arc_pen = None                   # 背景画笔

    # 喝水设置
    drinking_count = 8                          # 喝水杯数
    view_message = "positive"                   # 窗口信息 正着计数(positive)/倒着计数(negative)
    schedule = 0                                # 当前喝水杯数

    open_todo_data_list = [
        # id, 标题, 是否完成, 程度, 是否提醒, 提醒时间
        # ["4ab462c6-7474-426c-b033-6c41d48f4d20", "今天要把第三个任务整一整", False, "Second", False, "", ""],
        # ["be16457a-c9fa-45d8-927e-903733457302", "摸鱼！！！摸鱼！！！", False, "Third", True, "2024-05-14 00:00:00", ""],
        # ["1e16457a-c9fa-45d8-927e-903733457302", "摸鱼！！！摸鱼！！！", False, "Third", True, "2024-05-14 00:00:00", ""],
        # ["2e16457a-c9fa-45d8-927e-903733457302", "摸鱼！！！摸鱼！！！", False, "Third", True, "2024-05-14 00:00:00", ""],
        # ["3e16457a-c9fa-45d8-927e-903733457302", "摸鱼！！！摸鱼！！！", False, "Third", True, "2024-05-14 00:00:00", ""],
    ]
    close_todo_data_list = [
        # id, 标题, 是否完成, 程度, 是否提醒, 提醒时间
        # ["45d5f285-5f19-4b97-a13a-3ec64ab2a391", "今天要把第一个任务完成到100%", True, "First", False, "", ""],
        # ["25d5f285-5f19-4b97-a13a-3ec64ab2a391", "今天要把第二个任务完成到80%", True, "First", True, "2024-05-03 09:00:00", ""],
        # ["0ab462c6-7474-426c-b033-6c41d48f4d20", "第四个任务整不了一点", True, "Second", False, "", ""],
    ]
    open_todo_item_map = {}
    close_todo_item_map = {}
    open_todo_widget_item_list = []
    close_todo_widget_item_list = []

    def __init__(self, parent=None):
        super(MyForm, self).__init__(parent=parent)
        print("super success")
        # 样式
        # self.windowEffect.setAeroEffect(self.winId())     # 磨砂
        self.windowEffect.setAcrylicEffect(self.winId(), "F2F2F299", False, 0)   # 亚克力
        # self.windowEffect.setMicaEffect(self.winId())       # 云母
        # self.windowEffect.setTransparentEffect(self.winId())      # 透明,仅mac
        print("style success")
        # 设置标题栏文字
        self.setWindowTitle(self.app_name)
        print("title success")
        # 隐藏标题栏
        self.titleBar.raise_()
        self.titleBar.minBtn.close()
        self.titleBar.maxBtn.close()
        self.titleBar.closeBtn.hide()
        self.update()
        print("title bar success")
        # 亚克力 - 浅色
        # self.setWindowFlags(QtCore.Qt.SplashScreen | QtCore.Qt.WindowStaysOnTopHint)
        # self.setWindowFlags(QtCore.Qt.SplashScreen)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        print("flag first success")
        # 初始化图标和托盘图标
        icon_tool.set_icon(self)
        print("icon success")
        icon_tool.set_tray_icon(self)
        print("tray icon success")
        # 初始化界面
        self.setupUi(self)
        self.resize(445, 1032)
        print("size success")
        # 置底透明
        # self.setWindowFlags(QtCore.Qt.SplashScreen | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnBottomHint)
        # self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(QtCore.Qt.SplashScreen)
        print("flag second success")
        # 初始化分辨率参数
        resolution_util.init_resolution(self)
        print("resolution success")
        # 初始化位置和大小
        self.move(self.desktop_width - self.width(), 0)
        self.setFixedSize(self.width(), self.desktop_height - self.taskbar_height)
        print("location success")
        # 其余初始化
        init_module.init_module(self)
        print("init success")
        # 初始化菜单
        self.see_card = "weibo"
        self.show_change()
        self.push_button_drink.hide()
        print("all success")
        # 初始化待办清单
        self.todo_list_widget_todo.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.todo_list_widget_todo.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.todo_list_widget_success.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.todo_list_widget_success.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        todo_list_config_data = todo_list_config.get_todo_list_config()
        self.open_todo_data_list = todo_list_config_data['proceed_todo_list']
        self.close_todo_data_list = todo_list_config_data['complete_todo_list']
        for todo_id, title, success, degree, warn, time_str, des in self.open_todo_data_list:
            item = MyQWidgetItem(self.todo_list_widget_todo, todo_id, title, success, degree, warn, time_str)
            self.open_todo_item_map[todo_id] = item
            item.delete_button.clicked.connect(partial(self.todo_delete_click, todo_id, True))
            item.check_push_button.clicked.connect(partial(self.todo_checked_click, todo_id, True))
            widget_item = QListWidgetItem(self.todo_list_widget_todo)
            widget_item.setSizeHint(item.sizeHint())
            self.open_todo_widget_item_list.append(widget_item)
            self.todo_list_widget_todo.addItem(widget_item)
            self.todo_list_widget_todo.setItemWidget(widget_item, item)
        self.todo_list_widget_todo.itemDoubleClicked.connect(partial(self.todo_double_click, True))
        for todo_id, title, success, degree, warn, time_str, des in self.close_todo_data_list:
            item = MyQWidgetItem(self.todo_list_widget_success, todo_id, title, success, degree, warn, time_str)
            self.close_todo_item_map[todo_id] = item
            item.delete_button.clicked.connect(partial(self.todo_delete_click, todo_id, False))
            item.check_push_button.clicked.connect(partial(self.todo_checked_click, todo_id, False))
            widget_item = QListWidgetItem(self.todo_list_widget_success)
            widget_item.setSizeHint(item.sizeHint())
            self.close_todo_widget_item_list.append(widget_item)
            self.todo_list_widget_success.addItem(widget_item)
            self.todo_list_widget_success.setItemWidget(widget_item, item)
        self.todo_list_widget_success.itemDoubleClicked.connect(partial(self.todo_double_click, False))
        self.todo_list_widget_success.hide()
        # 隐藏没有实现的功能按钮
        self.push_button_about.hide()
        self.push_button_setting.hide()
        self.push_button_game.hide()
        self.push_button_novel.hide()
        # 默认微博
        self.push_button_weibo_click()

    '''
    **********************************待办清单点击***************************************
    ↓                                                                                 ↓
    '''
    def todo_delete_click(self, todo_id, open):
        if open:
            open_delete_index = None
            for todo_data_index in range(len(self.open_todo_data_list)):
                if todo_id == self.open_todo_data_list[todo_data_index][0]:
                    open_delete_index = todo_data_index
            del self.open_todo_data_list[open_delete_index]
            del self.open_todo_widget_item_list[open_delete_index]
            del self.open_todo_item_map[todo_id]
            self.todo_list_widget_todo.takeItem(open_delete_index)
        else:
            close_delete_index = None
            for todo_data_index in range(len(self.close_todo_data_list)):
                if todo_id == self.close_todo_data_list[todo_data_index][0]:
                    close_delete_index = todo_data_index
            del self.close_todo_data_list[close_delete_index]
            del self.close_todo_widget_item_list[close_delete_index]
            del self.close_todo_item_map[todo_id]
            self.todo_list_widget_success.takeItem(close_delete_index)
        todo_list_config.set_todo_list_config({"proceed_todo_list": self.open_todo_data_list,
                                               "complete_todo_list": self.close_todo_data_list})

    def todo_checked_click(self, todo_id, complete):
        if complete:
            # 从proceed中删除
            open_delete_index = None
            open_delete_data = None
            for todo_data_index in range(len(self.open_todo_data_list)):
                if todo_id == self.open_todo_data_list[todo_data_index][0]:
                    open_delete_index = todo_data_index
                    open_delete_data = self.open_todo_data_list[todo_data_index]
                    open_delete_data[2] = not open_delete_data[2]
            print("待办->完成" + str(open_delete_data))
            self.open_todo_item_map[todo_id].set_custom_success(open_delete_data[2])
            self.open_todo_data_list.remove(open_delete_data)
            del self.open_todo_widget_item_list[open_delete_index]
            del self.open_todo_item_map[todo_id]
            self.todo_list_widget_todo.takeItem(open_delete_index)
            # 加到complete中
            self.close_todo_data_list.append(open_delete_data)
            item = MyQWidgetItem(self.todo_list_widget_success, open_delete_data[0], open_delete_data[1], open_delete_data[2],
                                                       open_delete_data[3], open_delete_data[4], open_delete_data[5])
            self.close_todo_item_map[todo_id] = item
            item.delete_button.clicked.connect(partial(self.todo_delete_click, todo_id, False))
            item.check_push_button.clicked.connect(partial(self.todo_checked_click, todo_id, False))
            widget_item = QListWidgetItem(self.todo_list_widget_success)
            widget_item.setSizeHint(item.sizeHint())
            self.close_todo_widget_item_list.append(widget_item)
            self.todo_list_widget_success.addItem(widget_item)
            self.todo_list_widget_success.setItemWidget(widget_item, item)
        else:
            # 从complete中删除
            close_delete_index = None
            close_delete_data = None
            for todo_data_index in range(len(self.close_todo_data_list)):
                if todo_id == self.close_todo_data_list[todo_data_index][0]:
                    close_delete_index = todo_data_index
                    close_delete_data = self.close_todo_data_list[todo_data_index]
                    close_delete_data[2] = not close_delete_data[2]
            print("完成->待办" + str(close_delete_data))
            self.close_todo_item_map[todo_id].set_custom_success(close_delete_data[2])
            self.close_todo_data_list.remove(close_delete_data)
            del self.close_todo_widget_item_list[close_delete_index]
            del self.close_todo_item_map[todo_id]
            self.todo_list_widget_success.takeItem(close_delete_index)
            # 加到proceed中
            self.open_todo_data_list.append(close_delete_data)
            item = MyQWidgetItem(self.todo_list_widget_todo, close_delete_data[0], close_delete_data[1], close_delete_data[2],
                                                       close_delete_data[3], close_delete_data[4], close_delete_data[5])
            self.open_todo_item_map[todo_id] = item
            item.delete_button.clicked.connect(partial(self.todo_delete_click, todo_id, True))
            item.check_push_button.clicked.connect(partial(self.todo_checked_click, todo_id, True))
            widget_item = QListWidgetItem(self.todo_list_widget_todo)
            widget_item.setSizeHint(item.sizeHint())
            self.open_todo_widget_item_list.append(widget_item)
            self.todo_list_widget_todo.addItem(widget_item)
            self.todo_list_widget_todo.setItemWidget(widget_item, item)
        todo_list_config.set_todo_list_config({"proceed_todo_list": self.open_todo_data_list,
                                               "complete_todo_list": self.close_todo_data_list})

    def todo_double_click(self, item, open):
        if self.todo_list_widget_success.isHidden():
            double_index = self.todo_list_widget_todo.currentRow()
            print(self.open_todo_data_list[double_index])
            self.open_new_todo_view(self.open_todo_data_list[double_index])
        else:
            double_index = self.todo_list_widget_success.currentRow()
            print(self.close_todo_data_list[double_index])
            self.open_new_todo_view(self.close_todo_data_list[double_index])

    def open_todo_success_click(self):
        self.new_todo_win.input_data[1] = self.new_todo_win.line_edit_title.text()
        if self.new_todo_win.combo_box_degree.currentText() == "紧急":
            self.new_todo_win.input_data[3] = "First"
        elif self.new_todo_win.combo_box_degree.currentText() == "一般":
            self.new_todo_win.input_data[3] = "Second"
        elif self.new_todo_win.combo_box_degree.currentText() == "莫慌":
            self.new_todo_win.input_data[3] = "Third"
        if self.new_todo_win.check_push_button.text() == "":
            self.new_todo_win.input_data[4] = False
            self.new_todo_win.input_data[5] = ""
        else:
            self.new_todo_win.input_data[4] = True
            self.new_todo_win.input_data[5] = self.new_todo_win.date_time_edit.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        self.new_todo_win.input_data[6] = self.new_todo_win.text_edit_des.toPlainText()
        input_data = self.new_todo_win.input_data
        self.new_todo_win.close()
        if self.new_todo_win.input_data[0] is None or self.new_todo_win.input_data[0] == "":
            self.new_todo_win.input_data[0] = str(uuid.uuid4())
            self.todo_add(input_data)
        else:
            self.todo_edit(input_data)
        todo_list_config.set_todo_list_config({"proceed_todo_list": self.open_todo_data_list,
                                               "complete_todo_list": self.close_todo_data_list})

    def todo_edit(self, input_data):
        if not input_data[2]:
            print("todo_edit1:{}".format(str(self.open_todo_data_list)))
            open_checked_index = None
            for todo_data_index in range(len(self.open_todo_data_list)):
                if input_data[0] == self.open_todo_data_list[todo_data_index][0]:
                    open_checked_index = todo_data_index
            self.open_todo_data_list[open_checked_index] = input_data
            self.open_todo_item_map[input_data[0]].set_all(self, input_data[0], input_data[1], input_data[2],
                                                       input_data[3], input_data[4], input_data[5])
            if self.open_todo_data_list[open_checked_index][4]:
                self.open_todo_widget_item_list[open_checked_index].setSizeHint(QSize(374, 59))
            else:
                self.open_todo_widget_item_list[open_checked_index].setSizeHint(QSize(374, 49))
        else:
            print("todo_edit2:{}".format(str(self.close_todo_data_list)))
            close_checked_index = None
            for todo_data_index in range(len(self.close_todo_data_list)):
                if input_data[0] == self.close_todo_data_list[todo_data_index][0]:
                    close_checked_index = todo_data_index
            self.close_todo_data_list[close_checked_index] = input_data
            self.close_todo_item_map[input_data[0]].set_all(self, input_data[0], input_data[1], input_data[2],
                                                       input_data[3], input_data[4], input_data[5])
            if self.close_todo_data_list[close_checked_index][4]:
                self.close_todo_widget_item_list[close_checked_index].setSizeHint(QSize(374, 59))
            else:
                self.close_todo_widget_item_list[close_checked_index].setSizeHint(QSize(374, 49))

    def todo_add(self, input_data):
        todo_id = input_data[0]
        if not self.todo_list_widget_success.isHidden():
            input_data[2] = True
            self.close_todo_data_list.append(input_data)
            item = MyQWidgetItem(self.todo_list_widget_success, input_data[0], input_data[1], input_data[2],
                                                       input_data[3], input_data[4], input_data[5])
            self.close_todo_item_map[todo_id] = item
            item.delete_button.clicked.connect(partial(self.todo_delete_click, todo_id, False))
            item.check_push_button.clicked.connect(partial(self.todo_checked_click, todo_id, False))
            widget_item = QListWidgetItem(self.todo_list_widget_success)
            widget_item.setSizeHint(item.sizeHint())
            self.close_todo_widget_item_list.append(widget_item)
            self.todo_list_widget_success.addItem(widget_item)
            self.todo_list_widget_success.setItemWidget(widget_item, item)
        else:
            input_data[2] = False
            self.open_todo_data_list.append(input_data)
            item = MyQWidgetItem(self.todo_list_widget_todo, input_data[0], input_data[1], input_data[2],
                                                       input_data[3], input_data[4], input_data[5])
            self.open_todo_item_map[todo_id] = item
            item.delete_button.clicked.connect(partial(self.todo_delete_click, todo_id, True))
            item.check_push_button.clicked.connect(partial(self.todo_checked_click, todo_id, True))
            widget_item = QListWidgetItem(self.todo_list_widget_todo)
            widget_item.setSizeHint(item.sizeHint())
            self.open_todo_widget_item_list.append(widget_item)
            self.todo_list_widget_todo.addItem(widget_item)
            self.todo_list_widget_todo.setItemWidget(widget_item, item)

    def push_button_todo_open_click(self):
        self.todo_list_widget_todo.show()
        self.todo_list_widget_success.hide()
        self.set_todo_show("todo", self.push_button_todo_todo)

    def push_button_todo_close_click(self):
        self.todo_list_widget_todo.hide()
        self.todo_list_widget_success.show()
        self.set_todo_show("success", self.push_button_todo_ok)

    def set_todo_show(self, top_type, top_button):
        self.line_top_4.raise_()
        top_button.raise_()
        self.push_button_todo_todo.setStyleSheet(style_util.get_top_style("todo", top_type == "todo"))
        self.push_button_todo_ok.setStyleSheet(style_util.get_top_style("success", top_type == "success"))
        self.line_top_4.setStyleSheet(style_util.get_top_line_style(top_type))

    '''
    **********************************卡片 · 开始***************************************
    ↓                                                                                 ↓
    '''

    def show_change(self):
        # self.weibo_text_browser.hide()
        self.top_area.hide()
        self.scroll_area.hide()
        self.looking_area.hide()
        self.reading_area.hide()
        self.todo_area.hide()
        self.set_menu_style(self.push_button_weibo_info, False)
        self.set_menu_style(self.push_button_60s_news, False)
        self.set_menu_style(self.push_button_looking, False)
        self.set_menu_style(self.push_button_reading, False)
        self.set_menu_style(self.push_button_todo, False)
        # self.set_menu_style(self.push_button_todo, False)
        # self.set_menu_style(self.push_button_novel, False)
        # self.set_menu_style(self.push_button_game, False)
        # self.set_menu_style(self.push_button_setting, False)
        # self.set_menu_style(self.push_button_about, False)
        if self.see_card == "weibo":
            self.set_menu_style(self.push_button_weibo_info, True)
            # self.weibo_text_browser.show()
            self.top_area.show()
        elif self.see_card == "60s":
            self.set_menu_style(self.push_button_60s_news, True)
            self.scroll_area.show()
        elif self.see_card == "looking":
            self.set_menu_style(self.push_button_looking, True)
            self.looking_area.show()
        elif self.see_card == "reading":
            self.set_menu_style(self.push_button_reading, True)
            self.reading_area.show()
        elif self.see_card == "todo":
            self.set_menu_style(self.push_button_todo, True)
            self.todo_area.show()

    def set_menu_style(self, button, state):
        if state:
            button.setStyleSheet(style_util.get_menu_button_style(True))
            font = QtGui.QFont()
            font.setFamily("思源黑体")
            font.setPointSize(11)
            font.setBold(True)
            font.setWeight(75)
            font.setKerning(True)
            button.setFont(font)
        else:
            button.setStyleSheet(style_util.get_menu_button_style(False))
            font = QtGui.QFont()
            font.setFamily("思源黑体")
            font.setPointSize(10)
            button.setFont(font)

    def show_image_window(self, title, image_data):
        show_image_util.show_image_window(self, title, image_data)
    '''
    ↑                                                                                ↑
    **********************************卡片 · 结束***************************************
    '''

    def box_info(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        # 设置背景色为白色，字体颜色为黑色
        msg_box.setStyleSheet(
            "QMessageBox { background-color: white; }"
            "QLabel { color: black; }"
        )
        # 创建自定义中文按钮
        ok_button = msg_box.addButton("确认", QMessageBox.RejectRole)
        msg_box.setDefaultButton(ok_button)
        msg_box.exec_()

    def box_error(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        # 设置背景色为白色，字体颜色为黑色
        msg_box.setStyleSheet(
            "QMessageBox { background-color: white; }"
            "QLabel { color: black; }"
        )
        # 创建自定义中文按钮
        ok_button = msg_box.addButton("确认", QMessageBox.RejectRole)
        msg_box.setDefaultButton(ok_button)
        msg_box.exec_()

    '''
    ********************************卡片1微博 · 开始*************************************
    ↓                                                                                 ↓
    '''
    def push_button_weibo_click(self):
        try:
            res = get_micro_blog_info.get_base_info()
            weibo_html = ""
            if "403 Forbidden" in str(res.text):
                weibo_html = "获取微博失败"
            else:
                html = etree.HTML(res.text)  # 转化成html文件
                table = html.xpath("//table")[0]
                weibo_html = etree.tostring(table, encoding="utf-8", method='html')
                weibo_html = bytes.decode(weibo_html)
                weibo_html = get_micro_blog_info.change_css(weibo_html)
            self.weibo_text_browser.setHtml(weibo_html)
            self.info_logger.info("获取微博信息完成")
            self.see_card = "weibo"
            self.show_change()
            self.set_top_show("weibo", self.push_button_top_weibo)
            return True
        except Exception as e:
            self.info_logger.error("获取微博信息失败,错误信息:{}".format(e))
            self.box_error("错误信息", "获取微博信息失败,请稍后重试")
            return False

    def click_textbrowser(self, url):
        if "http" not in url.toString():
            browser_util.open_url("https://s.weibo.com/" + url.toString())
        browser_util.open_url(url.toString())

    def push_button_top_weibo_click(self):
        if self.push_button_weibo_click():
            self.set_top_show("weibo", self.push_button_top_weibo)

    def push_button_top_baidu_click(self):
        if self.get_base_top_info("baidu", "百度"):
            self.set_top_show("baidu", self.push_button_top_baidu)

    def push_button_top_bilibili_click(self):
        if self.get_base_top_info("bilibili", "Bilibili"):
            self.set_top_show("bilibili", self.push_button_top_bilibili)

    def push_button_top_zhihu_click(self):
        if self.get_base_top_info("zhihu", "知乎"):
            self.set_top_show("zhihu", self.push_button_top_zhihu)

    def push_button_top_douyin_click(self):
        if self.get_base_top_info("douyin", "抖音"):
            self.set_top_show("douyin", self.push_button_top_douyin)

    def push_button_top_tencent_click(self):
        if self.get_base_top_info("tencent", "腾讯"):
            self.set_top_show("tencent", self.push_button_top_tencent)

    def get_base_top_info(self, type_name, type_title):
        try:
            res = get_tophub_blog_info.get_base_info()
            if "403 Forbidden" in str(res.text):
                base_html = "获取" + type_title + "失败"
            else:
                base_html = get_tophub_blog_info.change_style(res, type_name, self.info_logger)
                base_html = get_micro_blog_info.change_css(base_html)
            self.weibo_text_browser.setHtml(base_html)
            self.info_logger.info("获取" + type_title + "信息完成")
            return True
        except Exception as e:
            self.info_logger.error("获取" + type_title + "信息失败,错误信息:{}".format(e))
            self.box_error("错误信息", "获取" + type_title + "信息失败,请稍后重试")
            return False

    def set_top_show(self, top_type, top_button):
        self.line_top.raise_()
        top_button.raise_()
        self.push_button_top_weibo.setStyleSheet(style_util.get_top_style("weibo", top_type == "weibo"))
        self.push_button_top_baidu.setStyleSheet(style_util.get_top_style("baidu", top_type == "baidu"))
        self.push_button_top_bilibili.setStyleSheet(style_util.get_top_style("bilibili", top_type == "bilibili"))
        self.push_button_top_zhihu.setStyleSheet(style_util.get_top_style("zhihu", top_type == "zhihu"))
        self.push_button_top_douyin.setStyleSheet(style_util.get_top_style("douyin", top_type == "douyin"))
        self.push_button_top_tencent.setStyleSheet(style_util.get_top_style("tencent", top_type == "tencent"))
        self.line_top.setStyleSheet(style_util.get_top_line_style(top_type))

    '''
    ↑                                                                                ↑
    *********************************卡片2微博 · 结束************************************
    '''

    '''
    ********************************卡片2读世界 · 开始************************************
    ↓                                                                                 ↓
    '''
    def push_button_60s_click(self):
        """
        方式1: requests.get('https://api.qqsuu.cn/api/dm-60s').content
        方式2: requests.get('http://bjb.yunwj.top/php/tp/60.jpg').content
        方式3: requests.get(requests.get('http://bjb.yunwj.top/php/tp/lj.php').json()['tp1']).content
        """
        get_success = False
        try:
            # 拉取60秒读懂世界的文字图片
            self.cache_label = MyQLabel(self)
            img = QtGui.QImage()
            img.loadFromData(requests.get('https://api.qqsuu.cn/api/dm-60s', timeout=1).content)
            pic = QtGui.QPixmap(img)
            pic.height()
            self.cache_label.setPixmap(pic)
            self.cache_label.setScaledContents(True)
            self.cache_label.setMaximumWidth(381)
            self.cache_label.setMaximumHeight(int(pic.height() / (pic.width() / 381)))
            self.scroll_area.setWidget(self.cache_label)
            self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.see_card = "60s"
            self.show_change()
            self.info_logger.info("获取秒读完成")
            get_success = True
        except Exception as e:
            self.info_logger.error("获取秒读分支1失败,错误信息:{}".format(e))
        if not get_success:
            try:
                # 拉取60秒读懂世界的文字图片
                self.cache_label = MyQLabel(self)
                img = QtGui.QImage()
                img.loadFromData(requests.get('http://bjb.yunwj.top/php/tp/60.jpg', timeout=1).content)
                pic = QtGui.QPixmap(img)
                pic.height()
                self.cache_label.setPixmap(pic)
                self.cache_label.setScaledContents(True)
                self.cache_label.setMaximumWidth(376)
                self.cache_label.setMaximumHeight(int(pic.height() / (pic.width() / 376)))
                self.scroll_area.setWidget(self.cache_label)
                self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                self.see_card = "60s"
                self.show_change()
                self.info_logger.info("获取秒读完成")
            except Exception as e:
                self.info_logger.error("获取秒读失败,错误信息:{}".format(e))
                self.box_error("错误信息", "获取秒读失败,请稍后重试")
    '''
    ↑                                                                                ↑
    *********************************卡片2读世界 · 开始***********************************
    '''

    '''
    ******************************卡片3 · Looking · 开始*********************************
    ↓                                                                                 ↓
    '''
    def push_button_looking_click(self):
        self.image_card_data = None
        self.see_card = "looking"
        self.show_change()

    def push_button_looking_fish_click(self):
        try:
            self.show_image_window("摸鱼人日历", requests.get(requests.get('https://dayu.qqsuu.cn/moyuribao/apis.php?type=json').json()['data']).content)
        except Exception as e:
            self.info_logger.error("获取摸鱼人日历失败,错误信息:{}".format(e))
            self.box_error("错误信息", "获取摸鱼人日历失败,请稍后重试")

    def push_button_looking_everyday_click(self):
        try:
            url = requests.get('https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1').json()['images'][0]['url']
            self.show_image_window("必应每日一图", requests.get("https://bing.com" + url).content)
        except Exception as e:
            self.info_logger.error("获取必应每日一图失败,错误信息:{}".format(e))
            self.box_error("错误信息", "获取必应每日一图失败,请稍后重试")

    def push_button_looking_girl_animation_click(self):
        try:
            self.show_image_window("摸鱼人日历", requests.get(requests.get('https://dayu.qqsuu.cn/moyuribao/apis.php?type=json').json()['data']).content)
        except Exception as e:
            self.info_logger.error("获取摸鱼人日历失败,错误信息:{}".format(e))
            self.box_error("错误信息", "获取摸鱼人日历失败,请稍后重试")

    def push_button_looking_girl_real_click(self):
        try:
            self.show_image_window("摸鱼人日历", requests.get(requests.get('https://dayu.qqsuu.cn/moyuribao/apis.php?type=json').json()['data']).content)
        except Exception as e:
            self.info_logger.error("获取摸鱼人日历失败,错误信息:{}".format(e))
            self.box_error("错误信息", "获取摸鱼人日历失败,请稍后重试")

    '''
    ↑                                                                                ↑
    ******************************卡片3 · Looking · 结束*********************************
    '''

    '''
    ******************************卡片4 · Reading · 开始*********************************
    ↓                                                                                 ↓
    '''
    def push_button_reading_click(self):
        self.image_card_data = None
        self.see_card = "reading"
        self.show_change()

    def push_button_reading_history_click(self):
        try:
            now = datetime.datetime.now()
            date_str = str(now.strftime("%m%d"))
            date_year = str(now.strftime("%Y"))
            result = requests.get('https://api.qqsuu.cn/api/dm-lishi?date=' + date_str).json()
            history_list = result['data']['list']
            history_str = ""
            for i in range(len(history_list)):
                history = history_list[len(history_list) - i - 1]
                history_date = history['lsdate']
                gap_year = int(date_year) - int(history_date[0:4])
                history_str += ("【" + history['lsdate'] + "  距今" + str(gap_year) + "年】" +
                                str(history['title']).replace("&nbsp;", " ") + "\r\n")
            self.box_info("历史上的今天", history_str)
        except Exception as e:
            self.info_logger.error("获取历史上的今天失败,错误信息:{}".format(e))
            self.box_error("错误信息", "获取历史上的今天失败,请稍后重试")

    def push_button_reading_life_click(self):
        try:
            result = requests.get('https://api.qqsuu.cn/api/dm-qiaomen').json()['data']['content']
            self.box_info("生活小窍门", result)
        except Exception as e:
            self.info_logger.error("获取生活小窍门失败,错误信息:{}".format(e))
            self.box_error("错误信息", "获取生活小窍门失败,请稍后重试")

    def push_button_reading_riddle_click(self):
        try:
            result = requests.get('https://api.qqsuu.cn/api/dm-naowan').json()
            riddle_list = result['data']['list']
            riddle_str = "问：\r\n"
            for i in range(len(riddle_list)):
                riddle_str += "【" + str(i + 1) + "】 " + riddle_list[i]['quest'] + "\r\n"
            riddle_str += "\r\n\r\n答：\r\n"
            for i in range(len(riddle_list)):
                riddle_str += "【" + str(i + 1) + "】 " + riddle_list[i]['result'] + "\r\n"
            self.box_info("脑筋急转弯", riddle_str)
        except Exception as e:
            self.info_logger.error("获取脑筋急转弯失败,错误信息:{}".format(e))
            self.box_error("错误信息", "获取脑筋急转弯失败,请稍后重试")

    def push_button_reading_rainbow_click(self):
        try:
            result = requests.get('https://api.qqsuu.cn/api/dm-caihongpi').json()['data']['content']
            self.box_info("彩虹屁", result)
        except Exception as e:
            self.info_logger.error("获取彩虹屁失败,错误信息:{}".format(e))
            self.box_error("错误信息", "获取彩虹屁失败,请稍后重试")

    def push_button_reading_morning_click(self):
        try:
            result = requests.get('https://api.qqsuu.cn/api/dm-zaoan').json()['data']['content']
            self.box_info("早安心语", result)
        except Exception as e:
            self.info_logger.error("获取早安心语失败,错误信息:{}".format(e))
            self.box_error("错误信息", "获取早安心语失败,请稍后重试")

    def push_button_reading_night_click(self):
        try:
            result = requests.get('https://api.qqsuu.cn/api/dm-wanan').json()['data']['content']
            self.box_info("晚安心语", result)
        except Exception as e:
            self.info_logger.error("获取晚安心语失败,错误信息:{}".format(e))
            self.box_error("错误信息", "获取晚安心语失败,请稍后重试")

    def push_button_reading_chicken_1_click(self):
        try:
            result = requests.get('https://api.qqsuu.cn/api/dm-dujitang').json()['msg']
            self.box_info("毒鸡汤①", result)
        except Exception as e:
            self.info_logger.error("获取毒鸡汤①失败,错误信息:{}".format(e))
            self.box_error("错误信息", "获取毒鸡汤①失败,请稍后重试")

    def push_button_reading_chicken_2_click(self):
        try:
            result = requests.get('https://api.qqsuu.cn/api/dm-djtang').json()['data']['content']
            self.box_info("毒鸡汤②", result)
        except Exception as e:
            self.info_logger.error("获取毒鸡汤②失败,错误信息:{}".format(e))
            self.box_error("错误信息", "获取毒鸡汤②失败,请稍后重试")

    def push_button_reading_cheesy_love_click(self):
        try:
            result = requests.get('https://api.qqsuu.cn/api/dm-saylove').json()['data']['content']
            self.box_info("土味情话", result)
        except Exception as e:
            self.info_logger.error("获取土味情话失败,错误信息:{}".format(e))
            self.box_error("错误信息", "获取土味情话失败,请稍后重试")
    '''
    ↑                                                                                ↑
    ******************************卡片4 · Reading · 结束*********************************
    '''


    '''
    ************************************待办事项 · 开始************************************
    ↓                                                                                   ↓
    '''
    def push_button_todo_click(self):
        try:
            self.info_logger.info("切换待办事项完成")
            self.see_card = "todo"
            self.show_change()
        except Exception as e:
            self.info_logger.error("切换待办事项失败,错误信息:{}".format(e))
            self.box_error("错误信息", "切换待办事项失败,请稍后重试")
    '''
    ↑                                                                                   ↑
    ************************************待办事项 · 结束************************************
    '''

    '''
    ********************************更新信息 · 开始**************************************
    ↓                                                                                 ↓
    '''
    def update_weather_info(self):
        city_config = city_setting.get_city_setting()
        if city_config is not None and "county" in city_config and city_config['county'] is not None and city_config['county'] != "":
            update_info_module.update_weather_info(self, city_code=int(city_config['county']))
            self.weather_position_label.setText("◉ " + city_config['countyName'])
        else:
            update_info_module.update_weather_info(self, city_code=101010100)
            self.weather_position_label.setText("◉ 北京")

    def update_date_and_time_model(self, update_time):
        update_info_module.update_date_and_time_model(self, update_time)

    def update_count_down_list_by_api(self):
        update_info_module.update_count_down_list_by_api(self)

    def time_trigger_update(self, datetime_now_str):
        update_info_module.time_trigger_update(self, datetime_now_str)
    '''
    ↑                                                                                ↑
    *********************************更新信息 · 结束*************************************
    '''

    '''
    **********************************喝水 · 开始***************************************
    ↓                                                                                 ↓
    '''
    def init_config(self):
        """
        初始化配置和喝水记录
        """
        drink_config = drinking_setting.get_drinking_setting()
        self.drinking_count = int(drink_config['drinking_count'])
        self.view_message = drink_config['view_message']
        drinking_data_list = drinking_config.get_drinking_config()
        if drinking_data_list is None or len(drinking_data_list) == 0:
            return
        today_str = str(datetime.date.today().strftime("%Y-%m-%d"))
        for drinking_data in drinking_data_list:
            if drinking_data['date'] == today_str:
                self.schedule = int(drinking_data['count'])
                return

    def push_button_add_click(self):
        self.schedule += 1
        drinking_config.set_drinking_config({
            "date": str(datetime.date.today().strftime("%Y-%m-%d")),
            "count": self.schedule
        })

    def push_button_clear_click(self):
        self.schedule = 0
        drinking_config.set_drinking_config({
            "date": str(datetime.date.today().strftime("%Y-%m-%d")),
            "count": self.schedule
        })

    # 打开设置界面
    def open_drinking_setting_view(self):
        self.setWindowFlag(Qt.WindowStaysOnTopHint, False)       # 窗口置顶
        self.show()
        if hasattr(self, "setting_win"):
            try:
                self.setting_win.close()
                self.setting_win = None
            except Exception:
                pass
        self.setting_win = SettingWindow()
        self.setting_win.setting_signal.connect(self.setting_update)
        self.setting_win.show()

    # 子页面信息显示方法
    def setting_update(self, info):
        self.init_config()

    # 打开记录界面
    def open_drinking_record_view(self):
        self.setWindowFlag(Qt.WindowStaysOnTopHint, False)       # 窗口置顶
        self.show()
        if hasattr(self, "record_win"):
            try:
                self.record_win.close()
                self.record_win = None
            except Exception:
                pass
        self.record_win = RecordWindow()
        self.record_win.show()

    # 打开记录界面
    def open_city_view(self):
        self.setWindowFlag(Qt.WindowStaysOnTopHint, False)       # 窗口置顶
        self.show()
        if hasattr(self, "city_win"):
            try:
                self.city_win.close()
                self.city_win = None
            except Exception:
                pass
        self.city_win = CityWindow()
        self.city_win.show()

    # 打开记录界面
    def open_new_todo_view(self, input=None):
        self.setWindowFlag(Qt.WindowStaysOnTopHint, False)       # 窗口置顶
        self.show()
        print("open_new_todo_view1:".format(str(self.close_todo_data_list)))
        if hasattr(self, "new_todo_win"):
            try:
                self.new_todo_win.close()
                self.new_todo_win = None
            except Exception:
                pass
        self.new_todo_win = NewTodoWindow(None, input)
        self.new_todo_win.push_button_success.clicked.connect(self.open_todo_success_click)
        self.new_todo_win.show()

    def paintEvent(self, event):
        if self.show_form:
            self.push_button_drink.hide()
            drink_paint.paintEvent(self, event)
        else:
            self.push_button_drink.show()
    '''
    ↑                                                                                ↑
    **********************************喝水 · 结束***************************************
    '''

    def showtime(self):
        """
        刷新时间
        :return:
        """
        self.time_label.setText("   " + str(datetime.datetime.now().strftime("%H  %M  %S")))
        self.update()

    def show_hide_form(self, click_button):
        """
        右键不处理动画
        :param click_button:
        :return:
        """
        if click_button == 1:
            return
        try:
            # 直接使用Qt方法置顶窗口
            self.raise_()
            self.activateWindow()
            self.showNormal()  # 避免使用Win32 API
        except Exception as e:
            print("快捷键进入退出动画失败,错误信息:{}".format(e))
        if self.show_form:
            resolution_util.out_animation(self)
        else:
            resolution_util.in_animation(self)
            self.refresh_window_show()

    def refresh_window_show(self):
        try:
            # 直接使用Qt方法置顶窗口
            self.raise_()
            self.activateWindow()
            self.showNormal()  # 避免使用Win32 API
        except Exception as e:
            pass
        # 窗口置顶
        self.setWindowFlag(Qt.WindowType.ToolTip)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

    def start_thread_list(self):
        """
        开始线程列表
        :return:
        """
        thread_util.close_one_thread(self.time_thread_object)
        self.time_thread_object = time_thread.TimeThread(self)
        self.time_thread_object.zero_trigger.connect(self.time_trigger_update)
        self.time_thread_object.setTerminationEnabled(True)
        self.time_thread_object.start()
        thread_util.close_one_thread(self.keyboard_thread_object)
        self.keyboard_thread_object = keyboard_thread.KeyboardThread(self)
        self.keyboard_thread_object.keyboard_trigger.connect(self.keyboard_active)
        self.keyboard_thread_object.setTerminationEnabled(True)
        self.keyboard_thread_object.start()

    def keyboard_active(self, event):
        """
        快捷键进入退出动画
        :return:
        """
        try:
            # 直接使用Qt方法置顶窗口
            self.raise_()
            self.activateWindow()
            self.showNormal()  # 避免使用Win32 API
        except Exception as e:
            print("快捷键进入退出动画失败,错误信息:{}".format(e))
        if self.show_form:
            resolution_util.out_animation(self)
        else:
            resolution_util.in_animation(self)
            self.refresh_window_show()

    def open_update_view(self):
        """
        更新记录
        :return:
        """
        self.box_info("更新记录", version_util.update_info)

    def open_about_view(self):
        """
        说明
        :return:
        """
        self.box_info("说明", version_util.about_info)

    def quit_before(self):
        """
        退出前置处理
        :return:
        """
        self.setVisible(False)
        thread_util.close_one_thread(self.time_thread_object)
        thread_util.close_one_thread(self.keyboard_thread_object)
        QApplication.instance().quit()

    def event(self, event):
        if QEvent.WindowDeactivate == event.type() or QEvent.ActivationChange == event.type():
            if QApplication.activeWindow() != self and self.show_form:
                resolution_util.out_animation(self)
        return super().event(event)

    def closeEvent(self, event):
        """
        最终退出
        :param event: QCloseEvent
        :return:
        """
        if event.type() == QEvent.Close:
            event.ignore()
        else:
            event.accept()


if __name__ == '__main__':
    print("start")
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    print("dpi success")
    app = QtWidgets.QApplication(sys.argv)
    print("app success")
    my_form = MyForm()
    print("form start")
    my_form.show()
    print("form end")
    sys.exit(app.exec_())
