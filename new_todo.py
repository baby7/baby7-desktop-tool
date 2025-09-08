# coding:utf-8
from PySide2 import QtCore
from PySide2.QtCore import Signal, QDateTime
from qframelesswindow import AcrylicWindow

from new_todo_form import Ui_Form


class NewTodoWindow(AcrylicWindow, Ui_Form):

    setting_signal = Signal(str)

    input_data = ["", "", False, "Third", False, "", ""]
    def __init__(self, parent=None, input_data=None):
        super(NewTodoWindow, self).__init__(parent=parent)
        self.input_data = ["", "", False, "First", False, "", ""]
        self.setupUi(self)
        self.setWindowFlag(QtCore.Qt.Tool)
        # 设置标题栏
        if input_data is not None:
            self.setWindowTitle("七仔的桌面工具 - 新建待办事项")
        else:
            self.setWindowTitle("七仔的桌面工具 - 编辑待办事项")
        self.titleBar.minBtn.close()
        self.titleBar.maxBtn.close()
        self.check_push_button.clicked.connect(self.todo_checked_click)
        self.push_button_cancel.clicked.connect(self.close)
        self.combo_box_degree.setCurrentText("莫慌")
        print(input_data)
        if input_data is not None:
            self.input_data = input_data
            self.line_edit_title.setText(input_data[1])
            self.text_edit_des.setText(input_data[6])
            if input_data[3] == "First":
                self.combo_box_degree.setCurrentText("紧急")
            elif input_data[3] == "Second":
                self.combo_box_degree.setCurrentText("一般")
            elif input_data[3] == "Third":
                self.combo_box_degree.setCurrentText("莫慌")
            if input_data[4]:
                self.check_push_button.setText("✓")
                self.check_push_button.setStyleSheet("border-style: solid;border-radius: 9px;border: 0px groove #000;\n"
                "color: rgb(255, 255, 255);border-color: rgba(0, 0, 0, 0.5);background-color: rgba(0, 0, 0, 0.5);")
            else:
                self.check_push_button.setText("")
                self.check_push_button.setStyleSheet("border-style: solid;border-radius: 9px;border: 1px groove #000;\n"
                "color: rgb(255, 255, 255);border-color: rgba(0, 0, 0, 0.5);background-color: rgb(255, 255, 255);")
            self.date_time_edit.setDateTime(QDateTime.fromString(input_data[5], 'yyyy-MM-dd hh:mm:ss'))

    def todo_checked_click(self):
        if self.check_push_button.text() == "":
            self.check_push_button.setText("✓")
            self.check_push_button.setStyleSheet("border-style: solid;border-radius: 9px;border: 0px groove #000;\n"
            "color: rgb(255, 255, 255);border-color: rgba(0, 0, 0, 0.5);background-color: rgba(0, 0, 0, 0.5);")
        else:
            self.check_push_button.setText("")
            self.check_push_button.setStyleSheet("border-style: solid;border-radius: 9px;border: 1px groove #000;\n"
            "color: rgb(255, 255, 255);border-color: rgba(0, 0, 0, 0.5);background-color: rgb(255, 255, 255);")
