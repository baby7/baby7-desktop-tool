# coding:utf-8
from PySide2.QtCore import Qt
from qframelesswindow import AcrylicWindow
from record_form import Ui_Form
from PySide2 import QtCore

from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

import config.drinking_config as drinking_config


class RecordWindow(AcrylicWindow, Ui_Form):

    def __init__(self, parent=None):
        super(RecordWindow, self).__init__(parent=parent)

        self.setupUi(self)
        self.setWindowFlag(QtCore.Qt.Tool)
        # 设置标题栏
        self.setWindowTitle("七仔的桌面工具 - 喝水记录")
        self.titleBar.minBtn.close()
        self.titleBar.maxBtn.close()
        drink_list = drinking_config.get_drinking_config()
        write_table_view(self.drink_table_view, drink_list,['日期', '杯数'], ['date', 'count'])
        self.drink_table_view.setColumnWidth(0, 130)
        self.drink_table_view.setColumnWidth(1, 80)


# 渲染列表
def write_table_view(table_view, data_list, title_list, name_list):
    model = QStandardItemModel(len(data_list), len(name_list))
    model.setHorizontalHeaderLabels(title_list)
    for row in range(len(data_list)):
        for line in range(len(name_list)):
            model.setItem(row, line, QStandardItem(str(data_list[row][name_list[line]])))
    table_view.setModel(model)
    # 设置滚动条
    table_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    # 设置表头不可点击
    table_view.horizontalHeader().setSectionsClickable(False)
    table_view.verticalHeader().setSectionsClickable(False)
    # 设置禁止编辑
    table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
    # 设置只能选中一行
    table_view.setSelectionMode(QAbstractItemView.SingleSelection)
    # 设置只能选中整行
    table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
    # 行高
    table_view.verticalHeader().setDefaultSectionSize(15)
