from PySide2 import QtWidgets
from PySide2.QtWidgets import *
from PySide2 import QtCore, QtGui


def set_card_location(card, sort, top):
    # x = 206
    x = 202
    y = top + int((int(sort / 2) - 1) * (12 + 71))
    if sort % 2 == 1:
        # x = 12
        x = 16
        y = top + int(int(sort / 2) * (12 + 71))
    card['title_label'].setText(card['title'])
    card['card_label'].setGeometry(QtCore.QRect(x, y, 181, 71))
    card['title_label'].setGeometry(QtCore.QRect(x + 8, y + 5, 161, 21))
    card['content_label'].setGeometry(QtCore.QRect(x + 8, y + 30, 161, 31))


def get_load_info_card(form, card_list, info_config, info_object):
    for card in card_list:
        if card['type'] == "info" and card['name'] == info_config['card']['file_name']:
            return card
    # 背景label
    card_label = QtWidgets.QLabel(form)
    card_label.setGeometry(QtCore.QRect(0, 0, 0, 0))
    font = QtGui.QFont()
    font.setFamily("思源黑体")
    font.setPointSize(10)
    card_label.setFont(font)
    # card_label.setStyleSheet("border-style: solid;\n"
    #                          "border-radius: 10px;\n"
    #                          "border: 0px groove gray;\n"
    #                          "color: rgb(0, 0, 0);\n"
    #                          "border-color: rgba(100, 100, 100, 0);\n"
    #                          "background-color: rgba(255, 255, 255, 1);")
    card_label.setStyleSheet("border-style: solid;\n"
                             "border-radius: 10px;\n"
                             "border: 1px groove gray;\n"
                             "color: rgb(0, 0, 0);\n"
                             "border-color: rgba(0, 0, 0, 0.5);\n"
                             "background-color: rgba(255, 255, 255, 1);")
    shadow = QGraphicsDropShadowEffect()
    shadow.setOffset(0, 0)  # 偏移
    shadow.setBlurRadius(1)  # 阴影半径
    # shadow.setColor(QtCore.Qt.white)  # 阴影颜色
    shadow.setColor(QtCore.Qt.black)  # 阴影颜色
    card_label.setGraphicsEffect(shadow)
    card_label.setText("")
    card_label.setAlignment(QtCore.Qt.AlignCenter)
    card_label.setObjectName("card_info_" + info_config['card']['file_name'])
    # 标题label
    title_label = QtWidgets.QLabel(form)
    title_label.setGeometry(QtCore.QRect(0, 0, 0, 0))
    font = QtGui.QFont()
    font.setFamily("思源黑体")
    font.setPointSize(10)
    title_label.setFont(font)
    title_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
    title_label.setObjectName("title_label_" + info_config['card']['file_name'])
    # 内容label
    content_label = QtWidgets.QLabel(form)
    content_label.setGeometry(QtCore.QRect(0, 0, 0, 0))
    content_label.setText("")
    content_label.setObjectName("content_label_" + info_config['card']['file_name'])
    card_list.append({
        "type": "info",
        "name": info_config['card']['file_name'],
        "title": info_config['card']['title'],
        "object": info_object(),
        "card_label": card_label,
        "title_label": title_label,
        "content_label": content_label
    })
    for card in card_list:
        if card['type'] == "info" and card['name'] == info_config['card']['file_name']:
            return card
