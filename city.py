# coding:utf-8
from PySide2 import QtCore
from PySide2.QtCore import Signal
from PySide2.QtWidgets import QMessageBox
from qframelesswindow import AcrylicWindow

import city_data
from city_form import Ui_Form
import config.city_setting as city_setting


class CityWindow(AcrylicWindow, Ui_Form):

    city_signal = Signal(str)

    city_message = city_data.city_message

    current_city_data = []

    current_province_code = None
    current_city_code = None
    current_county_code = None

    def __init__(self, parent=None, use_parent=None):
        super(CityWindow, self).__init__(parent=parent)

        self.setupUi(self)
        self.setWindowFlag(QtCore.Qt.Tool)
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
        self.use_parent = use_parent
        # 设置标题栏
        self.setWindowTitle("七仔的桌面工具 - 天气城市设置")
        self.titleBar.minBtn.close()
        self.titleBar.maxBtn.close()
        self.combo_box_province.addItem("--请选择省")
        self.combo_box_province.setStyleSheet(qssStyle)
        self.combo_box_city.addItem("--请选择市")
        self.combo_box_city.setStyleSheet(qssStyle)
        self.combo_box_county.addItem("--请选择县/区")
        self.combo_box_county.setStyleSheet(qssStyle)
        for data in self.city_message['CityCode']:
            self.combo_box_province.addItem(data['provinceName'])

    # 省选择器点击响应
    def slot_province_click(self, text):
        current_province = self.combo_box_province.currentText()
        if current_province.startswith('--') is True or current_province == "":
            print("请选择省")
            self.combo_box_city.clear()
            self.combo_box_county.clear()
            return
        print("选择的省为：" + current_province)
        for data in self.city_message['CityCode']:
            if data['provinceName'] != current_province:
                continue
            print("开始填充市选择器")
            self.current_province_code = data['provinceCode']
            self.combo_box_city.clear()
            self.current_city_data = data['cityList']
            city_count = 0
            for c in data['cityList']:
                self.combo_box_city.addItem(c['cityName'])
                city_count += 1
            print(f"市选择器填充完成,数量:{city_count}")

    # 市选择器点击响应
    def slot_city_click(self, text):
        current_city = self.combo_box_city.currentText()
        if current_city.startswith('--') is True or current_city == "":
            print("请选择市")
            self.combo_box_county.clear()
            return
        print("选择的市为：" + current_city)
        for data in self.current_city_data:
            if data['cityName'] != current_city:
                continue
            print("开始填充区/县选择器")
            self.current_city_code = data['cityCode']
            self.combo_box_county.clear()
            county_count = 0
            for c in data['countyList']:
                self.combo_box_county.addItem(c['name'])
                county_count += 1
            print(f"区/县选择器填充完成,数量:{county_count}")

    def push_button_ok_click(self):
        current_county = self.combo_box_county.currentText()
        current_county_code = None
        current_county_Name = None
        for data in self.city_message['CityCode']:
            if data['provinceCode'] == self.current_province_code:
                for c in data['cityList']:
                    if c['cityCode'] == self.current_city_code:
                        for cc in c['countyList']:
                            if cc['name'] == current_county:
                                current_county_code = cc['code']
                                current_county_Name = cc['name']
        if current_county_code is None:
            self.box_error("失败", "请选择正确的省市区")
            return
        city_setting.set_city_setting({
            'province': self.current_province_code,
            'city': self.current_city_code,
            'county': current_county_code,
            'countyName': current_county_Name
        })
        self.city_signal.emit('success')
        self.box_info("成功", "城市设置成功，会在十分钟内刷新，或重启刷新")
        return

    def box_info(self, title, message):
        msg_box = QMessageBox(self.use_parent)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        # 设置背景色为白色，字体颜色为黑色
        msg_box.setStyleSheet(
            "QMessageBox { background-color: white; }"
            "QLabel { color: black; }"
            "QPushButton { border-radius: 10px; border: 1px groove black; padding: 5px; }"
            "QPushButton:hover { border: 1px groove blue; }"
        )
        # 创建自定义中文按钮
        ok_button = msg_box.addButton("确认", QMessageBox.RejectRole)
        msg_box.setDefaultButton(ok_button)
        msg_box.exec_()

    def box_error(self, title, message):
        msg_box = QMessageBox(self.use_parent)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        # 设置背景色为白色，字体颜色为黑色
        msg_box.setStyleSheet(
            "QMessageBox { background-color: white; }"
            "QLabel { color: black; }"
            "QPushButton { border-radius: 10px; border: 1px groove black; padding: 5px; }"
            "QPushButton:hover { border: 1px groove blue; }"
        )
        # 创建自定义中文按钮
        ok_button = msg_box.addButton("确认", QMessageBox.RejectRole)
        msg_box.setDefaultButton(ok_button)
        msg_box.exec_()
