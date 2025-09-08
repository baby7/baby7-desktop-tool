# -- coding: utf-8 --
import os
import win32api
import traceback
from PySide2.QtCore import *
from config import start_module_list_config
from util import ip_change_util


# 启动模块线程
class StartModuleListThread(QThread):

    active = True                       # 线程是否需要保持执行
    error_trigger = Signal(str)     # 错误触发器
    now_start_model_title = "尚未开始"    # 当前启动的模块

    def __init__(self, parent=None):
        super().__init__(parent)

    def stop(self):
        self.terminate()

    """
    {
        start_module_list": [
            {
              "name": "ip_change",
              "type": "custom",
              "title": "host自动适应",
              "sort": 1
            },
            {
              "name": "AirLiveDrive",
              "type": "program",
              "title": "打开AirLiveDrive",
              "path": "E:\\soft\\AirLiveDrive\\AirLiveDrive.exe",
              "hide": 0,
              "sort": 2
            },
            {
              "name": "Clash",
              "type": "program",
              "title": "打开Clash",
              "path": "E:\\soft\\Clash for Windows\\Clash for Windows.exe",
              "hide": 0,
              "sort": 3
            }
          ]
    }
    """
    def run(self):
        start_module_list = start_module_list_config.get_start_module_list_config()['start_module_list']
        for start_module in start_module_list:
            if not self.active:
                break
            self.now_start_model_title = start_module['title']
            print("执行" + self.now_start_model_title)
            try:
                # 特定的 - host自适应
                if start_module['name'] == "ip_change":
                    ip_change_util.change()
                    continue
                # 打开程序
                if start_module['type'] == "program":
                    search_list = os.popen('tasklist | findstr ' + str(start_module['name'])).readlines()
                    if search_list is not None and len(search_list) > 0:
                        print("程序 " + self.now_start_model_title + " 已在运行，跳过")
                        continue
                    win32api.ShellExecute(0, 'open', start_module['path'], '', '', int(start_module['hide']))
                    continue
            except Exception:
                self.error_trigger.emit(self.now_start_model_title)
                traceback.print_exc()
