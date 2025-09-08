# coding:utf-8

from PySide2 import QtCore
from PySide2.QtCore import Signal
from PySide2.QtWidgets import QMessageBox
from qframelesswindow import AcrylicWindow

from setting_form import Ui_Form
import config.drinking_setting as drinking_setting


class SettingWindow(AcrylicWindow, Ui_Form):

    setting_signal = Signal(str)

    def __init__(self, parent=None):
        super(SettingWindow, self).__init__(parent=parent)

        self.setupUi(self)
        self.setWindowFlag(QtCore.Qt.Tool)

        # 设置标题栏
        self.setWindowTitle("七仔的桌面工具 - 喝水设置")
        self.titleBar.minBtn.close()
        self.titleBar.maxBtn.close()
        drink_config = drinking_setting.get_drinking_setting()
        self.spin_box_drinking_count.setValue(int(drink_config['drinking_count']))
        view_message = drink_config['view_message']
        view_message_str = "正着计数" if view_message == "positive" else "倒着计数"
        self.combo_box_view_message.setCurrentText(view_message_str)
        qssStyle = '''
            QComboBox {
                color: black;
                border-radius: 3px;
                border: 1px groove gray;
                color: rgb(0, 0, 0);
                border-color: rgb(0, 0, 0);
                background-color: rgb(255, 255, 255);
            }
        '''
        self.combo_box_view_message.setStyleSheet(qssStyle)

    def push_button_ok_click(self):
        view_message_str = self.combo_box_view_message.itemText(self.combo_box_view_message.currentIndex())
        view_message = "positive" if view_message_str == "正着计数" else "negative"
        drink_config = {
            "drinking_count": int(self.spin_box_drinking_count.text()),     # 喝水数量
            "view_message": view_message,                                   # 窗口信息 正着计数(positive)/倒着计数(negative)
        }
        drinking_setting.set_drinking_setting(drink_config)
        self.setting_signal.emit('success')
        self.box_info("成功", "喝水设置成功")

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

