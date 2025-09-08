# -*- coding: utf-8 -*-
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import *
from PySide2.QtCore import Qt


def get_font(family, size):
    font = QtGui.QFont()
    font.setFamily(family)
    font.setPointSize(size)
    return font


class MyQWidgetItem(QWidget):

    label_title = None
    blank_left_label = None
    check_push_button = None
    delete_button = None
    degree_line = None
    blank_label = None
    warn_label = None
    separation_line = None

    def __init__(self, parent=None, todo_id="", title="", success=False, degree="First", warn=False, time_str=""):
        super(MyQWidgetItem, self).__init__(parent)
        self.todo_id = todo_id
        # 标题
        self.label_title = QtWidgets.QLabel(parent)
        self.label_title.setFont(get_font("思源黑体", 11))
        self.label_title.setMinimumWidth(260)
        self.label_title.setMaximumHeight(23)
        self.label_title.setStyleSheet("border: 0px solid #FF8D16;border-radius: 0px;background-color: rgba(0, 0, 0, 0);")
        self.label_title.setText(title)
        # 勾选框左边的的占位
        self.blank_left_label = QtWidgets.QLabel(parent)
        self.blank_left_label.setFixedSize(5, 10)
        self.blank_left_label.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.blank_left_label.setText("")
        # 勾选框
        self.check_push_button = QtWidgets.QPushButton(parent)
        self.check_push_button.setFixedSize(18, 18)
        self.check_push_button.setFont(get_font("思源黑体", 9))
        self.check_push_button.setIconSize(QtCore.QSize(14, 14))
        if success:
            self.check_push_button.setText("✓")
            self.check_push_button.setStyleSheet("border-style: solid;border-radius: 9px;border: 0px groove #000;\n"
            "color: rgb(255, 255, 255);border-color: rgba(0, 0, 0, 0.5);background-color: rgba(0, 0, 0, 0.5);")
        else:
            self.check_push_button.setText("")
            self.check_push_button.setStyleSheet("border-style: solid;border-radius: 9px;border: 1px groove #000;\n"
            "color: rgb(255, 255, 255);border-color: rgba(0, 0, 0, 0.5);background-color: rgb(255, 255, 255);")
        # 删除按钮
        self.delete_button = QtWidgets.QPushButton(parent)
        self.delete_button.setFixedSize(25, 25)
        font = get_font("幼圆", 13)
        font.setBold(True)
        font.setWeight(75)
        self.delete_button.setFont(font)
        self.delete_button.setStyleSheet("color: rgb(166, 166, 166);")
        self.delete_button.setText("×")
        # 程度条
        self.degree_line = QtWidgets.QFrame(parent)
        if warn:
            self.degree_line.setFixedSize(6, 50)
        else:
            self.degree_line.setFixedSize(6, 40)
        self.degree_line.setFrameShape(QtWidgets.QFrame.VLine)
        self.degree_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        if degree == "First":
            self.degree_line.setStyleSheet("border-style: solid;border-radius: 3px;color: rgba(212, 63, 54, 0.8);\n"
            "border-color: rgba(212, 63, 54, 0.8);background-color: rgba(212, 63, 54, 0.8);")
        elif degree == "Second":
            self.degree_line.setStyleSheet("border-style: solid;border-radius: 3px;color: rgba(255, 139, 42, 0.8);\n"
            "border-color: rgba(255, 139, 42, 0.8);background-color: rgba(255, 139, 42, 0.8);")
        elif degree == "Third":
            self.degree_line.setStyleSheet("border-style: solid;border-radius: 3px;color: rgba(164, 207, 48, 0.8);\n"
            "border-color: rgba(164, 207, 48, 0.8);background-color: rgba(164, 207, 48, 0.8);")
        # 提醒时间
        if warn:
            # 勾选框下的占位
            self.blank_label = QtWidgets.QLabel(parent)
            self.blank_label.setFixedSize(1, 10)
            self.blank_label.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
            self.blank_label.setText("")
            # 提醒时间
            self.warn_label = QtWidgets.QLabel(parent)
            self.warn_label.setFixedSize(160, 18)
            self.warn_label.setFont(get_font("思源黑体", 9))
            self.warn_label.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
            self.warn_label.setText("🔔 " + time_str[:16])
        # 分隔符
        self.separation_line = QtWidgets.QFrame(parent)
        self.separation_line.setFixedSize(374, 1)
        self.separation_line.setMaximumHeight(1)
        self.separation_line.setStyleSheet("color: rgba(200, 200, 200, 0.3);border-color: rgba(200, 200, 200, 0.3);"
                                   "background-color: rgba(200, 200, 200, 0.3);")
        self.separation_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.separation_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        # 布局
        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.setContentsMargins(0, 4, 0, 0)
        self.main_layout.addWidget(self.degree_line)
        self.main_layout.addWidget(self.blank_left_label)
        self.check_and_blank_layout = QtWidgets.QVBoxLayout()
        self.check_and_blank_layout.setContentsMargins(0, 0, 0, 0)
        if warn:
            self.check_and_blank_layout.addWidget(self.check_push_button)
            self.check_and_blank_layout.addWidget(self.blank_label)
        else:
            self.check_and_blank_layout.addWidget(self.check_push_button)
        self.main_layout.addLayout(self.check_and_blank_layout)
        self.title_and_warn_layout = QtWidgets.QVBoxLayout()
        self.title_and_warn_layout.setContentsMargins(0, 0, 0, 0)
        if warn:
            self.title_and_warn_layout.addWidget(self.label_title)
            self.title_and_warn_layout.addWidget(self.warn_label)
        else:
            self.title_and_warn_layout.addWidget(self.label_title)
        self.main_layout.addLayout(self.title_and_warn_layout)
        self.main_layout.addWidget(self.delete_button)
        self.main_layout.setAlignment(self.delete_button, Qt.AlignCenter)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addLayout(self.main_layout)
        self.layout.addWidget(self.separation_line)
        self.setLayout(self.layout)

    def set_custom_title(self, text):
        self.label_title.setText(text)

    def set_custom_success(self, success):
        if success:
            self.check_push_button.setText("✓")
            self.check_push_button.setStyleSheet("border-style: solid;border-radius: 9px;border: 0px groove #000;\n"
            "color: rgb(255, 255, 255);border-color: rgba(0, 0, 0, 0.5);background-color: rgba(0, 0, 0, 0.5);")
        else:
            self.check_push_button.setText("")
            self.check_push_button.setStyleSheet("border-style: solid;border-radius: 9px;border: 1px groove #000;\n"
            "color: rgb(255, 255, 255);border-color: rgba(0, 0, 0, 0.5);background-color: rgb(255, 255, 255);")

    def set_custom_degree(self, degree):
        if degree == "First":
            self.degree_line.setStyleSheet("border-style: solid;border-radius: 3px;color: rgba(212, 63, 54, 0.8);\n"
            "border-color: rgba(212, 63, 54, 0.8);background-color: rgba(212, 63, 54, 0.8);")
        elif degree == "Second":
            self.degree_line.setStyleSheet("border-style: solid;border-radius: 3px;color: rgba(255, 139, 42, 0.8);\n"
            "border-color: rgba(255, 139, 42, 0.8);background-color: rgba(255, 139, 42, 0.8);")
        elif degree == "Third":
            self.degree_line.setStyleSheet("border-style: solid;border-radius: 3px;color: rgba(164, 207, 48, 0.8);\n"
            "border-color: rgba(164, 207, 48, 0.8);background-color: rgba(164, 207, 48, 0.8);")

    def set_all(self, parent=None, todo_id="", title="", success=False, degree="First", warn=False, time_str=""):
        self.todo_id = todo_id
        # 标题
        self.label_title.setText(title)
        # 勾选框
        if success:
            self.check_push_button.setText("✓")
            self.check_push_button.setStyleSheet("border-style: solid;border-radius: 9px;border: 0px groove #000;\n"
            "color: rgb(255, 255, 255);border-color: rgba(0, 0, 0, 0.5);background-color: rgba(0, 0, 0, 0.5);")
        else:
            self.check_push_button.setText("")
            self.check_push_button.setStyleSheet("border-style: solid;border-radius: 9px;border: 1px groove #000;\n"
            "color: rgb(255, 255, 255);border-color: rgba(0, 0, 0, 0.5);background-color: rgb(255, 255, 255);")
        # 程度条
        if warn:
            self.degree_line.setFixedSize(6, 50)
        else:
            self.degree_line.setFixedSize(6, 40)
        if degree == "First":
            self.degree_line.setStyleSheet("border-style: solid;border-radius: 3px;color: rgba(212, 63, 54, 0.8);\n"
            "border-color: rgba(212, 63, 54, 0.8);background-color: rgba(212, 63, 54, 0.8);")
        elif degree == "Second":
            self.degree_line.setStyleSheet("border-style: solid;border-radius: 3px;color: rgba(255, 139, 42, 0.8);\n"
            "border-color: rgba(255, 139, 42, 0.8);background-color: rgba(255, 139, 42, 0.8);")
        elif degree == "Third":
            self.degree_line.setStyleSheet("border-style: solid;border-radius: 3px;color: rgba(164, 207, 48, 0.8);\n"
            "border-color: rgba(164, 207, 48, 0.8);background-color: rgba(164, 207, 48, 0.8);")
        # 提醒时间
        if warn:
            if self.blank_label is None:
                # 勾选框下的占位
                self.blank_label = QtWidgets.QLabel(parent)
                self.blank_label.setFixedSize(1, 10)
                self.blank_label.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
                self.blank_label.setText("")
                # 提醒时间
                self.warn_label = QtWidgets.QLabel(parent)
                self.warn_label.setFixedSize(160, 18)
                self.warn_label.setFont(get_font("思源黑体", 9))
                self.warn_label.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
                self.warn_label.setText("🔔 " + time_str[:16])
                self.check_and_blank_layout.addWidget(self.blank_label)
                self.title_and_warn_layout.addWidget(self.warn_label)
            else:
                self.warn_label.setText("🔔 " + time_str[:16])
        else:
            if self.blank_label is not None:
                self.check_and_blank_layout.removeWidget(self.blank_label)
                self.title_and_warn_layout.removeWidget(self.warn_label)
                self.blank_label.clear()
                self.blank_label = None
                self.warn_label.clear()
                self.warn_label = None