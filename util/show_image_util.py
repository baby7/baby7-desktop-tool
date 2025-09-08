import os
from PySide2.QtWidgets import QApplication, QLabel, QDialog
from PySide2.QtGui import QPixmap

def show_image_window(main_object, title, image_data):
    try:
        if image_data is None:
            return
        desktop = QApplication.desktop().screenGeometry(0)  # 多显示屏，显示主屏
        desktop_width = desktop.width()
        desktop_height = desktop.height() - 100
        with open('collection.jpg', 'wb') as tmp:
            tmp.write(image_data)
            main_object.dialog_fault = QDialog()
            main_object.dialog_fault.setWindowTitle(title)
            image_path = "collection.jpg"
            pic = QPixmap(image_path)
            width = pic.width()
            height = pic.height()
            if width > desktop_width:
                height = int((desktop_width / width) * height)
                width = desktop_width
            if height > desktop_height:
                width = int((desktop_height / height) * width)
                height = desktop_height
            label_pic = QLabel("show", main_object.dialog_fault)
            label_pic.setPixmap(pic)
            label_pic.setGeometry(0, 0, width, height)
            label_pic.setScaledContents(True)
            main_object.dialog_fault.exec_()
        os.remove("collection.jpg")
    except Exception as e:
        print(e)