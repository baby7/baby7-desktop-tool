import time
import traceback
import requests
from PySide2.QtCore import *


# 加载图片
def set_data(url, label_data):
    try:
        response = requests.get(url)
        label_data['byte'] = QByteArray(response.content)
    except Exception as e:
        traceback.print_exc()


class ImgThread(QThread):
    active = True
    # 触发器
    end_trigger = Signal(dict)          # 使用结束触发器

    # 图片地址
    image_url_data_list = None
    label_image_data = None

    def __init__(self, parent=None, url_data=None):
        super().__init__(parent)
        self.image_url_data_list = url_data

    def stop(self):
        self.terminate()

    def run(self):
        for img_url_data in self.image_url_data_list:
            self.label_image_data = {
                "byte": None,
                "buffer": None,
                "gif": None,
                "name": img_url_data['name']
            }
            set_data(img_url_data['url'], self.label_image_data)
            self.end_trigger.emit(self.label_image_data)
            if not self.active:
                return
        time.sleep(1)
