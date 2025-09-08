import os
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (QMenu, QAction, QSystemTrayIcon)


# 设置图标
def set_icon(main_object):
    main_object.sys_icon = QIcon(":img/icon/icon.ico")
    main_object.setWindowIcon(main_object.sys_icon)


# 设置托盘图标
def set_tray_icon(main_object):
    menu = QMenu(main_object)
    menu.addAction(QAction(u'城市选择', main_object, triggered=main_object.open_city_view))
    menu.addAction(QAction(u'喝水设置', main_object, triggered=main_object.open_drinking_setting_view))
    menu.addAction(QAction(u'喝水记录', main_object, triggered=main_object.open_drinking_record_view))
    menu.addAction(QAction(u'更新记录', main_object, triggered=main_object.open_update_view))
    menu.addAction(QAction(u'说明', main_object, triggered=main_object.open_about_view))
    menu.addAction(QAction(u'退出', main_object, triggered=main_object.quit_before))
    menu.setStyleSheet("background: rgb(255, 255, 255); color: rgb(0, 0, 0);")
    main_object.tray_icon = QSystemTrayIcon(main_object)
    main_object.tray_icon.setIcon(main_object.sys_icon)
    main_object.tray_icon.setContextMenu(menu)
    main_object.tray_icon.activated.connect(main_object.show_hide_form)
    main_object.tray_icon.show()
